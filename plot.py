import pandas as pd
import matplotlib.pyplot as plt

# Load DataFrame
rtoi_df = pd.read_csv('data/plot-data.csv')
rtoi_df['Date'] = pd.to_datetime(rtoi_df['Date'], format='%Y/%m/%d')

# Plotting TW 10-Year Treasury Bond Rate
plt.figure()
plt.plot(rtoi_df['Date'], rtoi_df['Rf'], color='black', linewidth=1.5)
plt.xlabel("")
plt.ylabel("")
plt.tick_params(axis='both', which='both', length=0.02)
plt.xticks(rotation=90)
plt.legend(["TW 10-Year Treasury Bond Rate"], loc='upper right', prop={'size': 15})
plt.tight_layout()
plt.savefig("ovx-py-repo/plots/tw10y-treasurybdrate.png")
plt.close()


# Plotting TSEC weighted index
plt.figure()
plt.plot(rtoi_df['Date'], rtoi_df['TWII'], color='black', linewidth=1.5)
plt.xlabel("")
plt.ylabel("")
plt.tick_params(axis='both', which='both', length=0.02)
plt.xticks(rotation=90)
plt.legend(["TSEC weighted index"], loc='upper left', prop={'size': 15})
plt.tight_layout()
plt.savefig("ovx-py-repo/plots/tsec-weighted-index.png")
plt.close()

# Plotting CBOE Crude Oil Volatility Index
plt.figure()
plt.plot(rtoi_df['Date'], rtoi_df['OVX'], color='black', linewidth=1.5)
plt.xlabel("")
plt.ylabel("")
plt.tick_params(axis='both', which='both', length=0.02)
plt.xticks(rotation=90)
plt.legend(["CBOE Crude Oil Volatility Index"], loc='upper left', prop={'size': 15})
plt.tight_layout()
plt.savefig("ovx-py-repo/plots/ovx-index.png")
plt.close()

