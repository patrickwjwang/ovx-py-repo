import statsmodels.api as sm
import pandas as pd
import numpy as np
import ovx_data
from ovx_data import twii_df, fx_df, ovx_df
from ovx_data import individual_df

# Model OVX movement on aggregate stock return

## 3.1 Base Model
### Align the dataframes by date index and drop rows with missing data
merged_df = pd.concat([twii_df['mktprem'], fx_df['Close']], axis=1, keys=['mkt_rt', 'fx'])
merged_df.dropna(inplace=True)

### Create lagged variable for twii_df['pct_return']
merged_df['lag_mkt_rt'] = merged_df['mkt_rt'].shift(1)

### Drop any rows with NaN values (due to lagged variables or otherwise)
merged_df.dropna(inplace=True)

### Separate independent and dependent variables
X = merged_df[['fx', 'lag_mkt_rt']]
y = merged_df['mkt_rt']

### Add a constant (intercept) to the independent variables
X = sm.add_constant(X)

### Run the regression
model = sm.OLS(y, X)
result0 = model.fit()

## 3.2 Symmetric Impact
merged_df = pd.concat([twii_df['mktprem'], fx_df['Close'], ovx_df['diff']], axis=1, keys=['mkt_rt', 'fx', 'ovx_diff'])
merged_df.dropna(inplace=True)
merged_df['lag_mkt_rt'] = merged_df['mkt_rt'].shift(1)
merged_df.dropna(inplace=True)
X = merged_df[['fx', 'lag_mkt_rt', 'ovx_diff']]
X = sm.add_constant(X)
y = merged_df['mkt_rt']
model = sm.OLS(y, X)
result1 = model.fit()

## 3.3 Asymmetric Impact
merged_df = pd.concat([twii_df['mktprem'], fx_df['Close'], ovx_df['diff_pos'], ovx_df['diff_neg'], ], 
                        axis=1, keys=['mkt_rt', 'fx', 'ovx_pos_diff', 'ovx_neg_diff'])
merged_df.dropna(inplace=True)
merged_df['lag_mkt_rt'] = merged_df['mkt_rt'].shift(1)
merged_df.dropna(inplace=True)
X = merged_df[['fx', 'lag_mkt_rt', 'ovx_pos_diff', 'ovx_neg_diff']]
X = sm.add_constant(X)
y = merged_df['mkt_rt']
model = sm.OLS(y, X)
result2 = model.fit()


# 4. Model OVX movement on individual stock return

## 4.1 Post-ranking quartly Jensen’s alpha
beta_mkt_df = pd.DataFrame()
beta_ovx_df = pd.DataFrame()
agg_df = pd.concat([twii_df['mktprem'], ovx_df['diff']], axis=1, keys=['mkt_rt', 'ovx_diff'])
agg_df.dropna(inplace=True)
merged_df = pd.merge(agg_df, individual_df, left_index=True, right_index=True, how='inner')
merged_df.fillna(0, inplace=True)

## Variables
num_ind = 105
quarter = 63
N = int(np.floor(merged_df.shape[0] / quarter))  # N = 45

## Regression for individual stock
for i in range(num_ind):
    for j in range(N):
        start = j * quarter
        end = (j + 1) * quarter

        stock_ij = merged_df.iloc[start:end, i + 2]  # Y
        mkt_i = merged_df.iloc[start:end, 0]  # X1
        ovx_i = merged_df.iloc[start:end, 1]  # X2
        
        X = pd.concat([mkt_i, ovx_i], axis=1)
        X = sm.add_constant(X)        
        model = sm.OLS(stock_ij, X).fit() 

        coef_agg_ij = model.params[1]
        coef_ovx_ij = model.params[2]        
        beta_mkt_df.loc[i, j] = coef_agg_ij
        beta_ovx_df.loc[i, j] = coef_ovx_ij

## Calculate post ranking Jensen's alpha
alpha_df = pd.DataFrame(columns=['TOP Alpha', 'MID Alpha', 'BOT Alpha'])
ind_tercile = int(num_ind / 3)  # Number of stock per tercile = 35
for t in range(N):
    sorted_ovx_t = beta_ovx_df.iloc[:, t].sort_values(ascending=False) 
    top = sorted_ovx_t.index[:ind_tercile]
    mid = sorted_ovx_t.index[ind_tercile:ind_tercile*2]
    bot = sorted_ovx_t.index[ind_tercile*2:num_ind]
    
    start = t * quarter
    end = (t + 1) * quarter
    
    port_df = pd.DataFrame({
        'Mkt': merged_df.iloc[start:end, 0]
    })
    
    port_df['TOP'] = merged_df.iloc[start:end, top + 2].mean(axis=1) 
    port_df['MID'] = merged_df.iloc[start:end, mid + 2].mean(axis=1) 
    port_df['BOT'] = merged_df.iloc[start:end, bot + 2].mean(axis=1)

    for portfolio in ['TOP', 'MID', 'BOT']:
        X = sm.add_constant(port_df['Mkt'])
        y = port_df[portfolio]
        
        model = sm.OLS(y, X).fit()
        alpha = model.params[0]        
        alpha_df.loc[t, f"{portfolio} Alpha"] = alpha

## Generate result table
alpha_result_df = pd.DataFrame({
        'Statistics': ['Top Tercile Alpha', 'Middle Tercile Alpha', 'Bottom Tercile Alpha'],
        'N': [N, N, N],
        'Mean': [alpha_df['TOP Alpha'].mean(), alpha_df['MID Alpha'].mean(), alpha_df['BOT Alpha'].mean()],
        'Std.Dev': [alpha_df['TOP Alpha'].std(), alpha_df['MID Alpha'].std(), alpha_df['BOT Alpha'].std()],
        'Min': [alpha_df['TOP Alpha'].min(), alpha_df['MID Alpha'].min(), alpha_df['BOT Alpha'].min()],
        'Max': [alpha_df['TOP Alpha'].max(), alpha_df['MID Alpha'].max(), alpha_df['BOT Alpha'].max()]
    })


## 4.2 Impact on individual stock return
### Calculate the return for entire period
df_modified = individual_df.applymap(lambda x: 1 + (x/100))
entire_ruturn = df_modified.prod(axis=0)*100  # 105 x 1 df
entire_ruturn.name = 'pct_return'
ind_return = entire_ruturn.to_frame()
ind_return = ind_return.reset_index()

beta_df = pd.DataFrame({
    'Intercept': [0] * 105,
    'Beta_MKT': [0] * 105,
    'Beta_OVX': [0] * 105,
    'Stock_Return': ind_return['pct_return']
})

## Individual regression
agg = merged_df.iloc[:, 0]
ovx = merged_df.iloc[:, 1]

for i in range(num_ind):
    stock_i = merged_df.iloc[:, i + 2]
    X = pd.concat([agg, ovx], axis=1)
    X = sm.add_constant(X)  # Adding a constant term for intercept
    lm_i = sm.OLS(stock_i, X).fit()
    beta_df.loc[i, 'Intercept'] = lm_i.params[0]
    beta_df.loc[i, 'Beta_MKT'] = lm_i.params[1]
    beta_df.loc[i, 'Beta_OVX'] = lm_i.params[2]

## Fama-Macbeth Regression
X = beta_df[['Beta_MKT', 'Beta_OVX']]
X = sm.add_constant(X)
lm_price = sm.OLS(beta_df['Stock_Return'], X).fit()

