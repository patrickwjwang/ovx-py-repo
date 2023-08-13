import pandas as pd
import numpy as np
import statsmodels.api as sm

# Load dataframe
agg_df = pd.read_csv("ovx-py-repo/data/agg.csv")
agg_df['Date'] = pd.to_datetime(agg_df['Date'], format='%Y/%m/%d')

aggRun_df = pd.DataFrame({
    'Date': agg_df['Date'].iloc[2:2842].tolist(),
    'MktPrem': agg_df['MktPrem_R'].iloc[2:2842].tolist(),
    'LagMktPrem': agg_df['MktPrem_R'].iloc[1:2841].tolist(),
    'FX': agg_df['FX_R'].iloc[2:2842].tolist(),
    'OVX': agg_df['OVX_C'].iloc[1:2841].tolist(),
    'OVX_P': agg_df['OVX_PC'].iloc[1:2841].tolist(),
    'OVX_N': agg_df['OVX_NC'].iloc[1:2841].tolist()
})


# Regression
X0 = sm.add_constant(aggRun_df[['FX', 'LagMktPrem']])
agg_lm0 = sm.OLS(aggRun_df['MktPrem'], X0).fit()

X1 = sm.add_constant(aggRun_df[['FX', 'LagMktPrem', 'OVX']])
agg_lm1 = sm.OLS(aggRun_df['MktPrem'], X1).fit()

X2 = sm.add_constant(aggRun_df[['FX', 'LagMktPrem', 'OVX_P', 'OVX_N']])
agg_lm2 = sm.OLS(aggRun_df['MktPrem'], X2).fit()

# Print regression results
print(agg_lm0.summary())
print(agg_lm1.summary())
print(agg_lm2.summary())
