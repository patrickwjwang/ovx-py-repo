## Overview
This repository contains Python code and data analysis scripts investigating the relationship between the Crude Oil Volatility Index (OVX) and the performance of the Taiwanese stock market. This research is aimed at providing insights into the impact of oil price volatility on Taiwan's aggregate stock returns, the risk premiums associated with oil volatility, and the market's sectoral exposure to oil volatility.

## Project Structure
`data/`: Contains raw and processed data files
`top_ticker_symbols.csv`: List of top 105 Taiwanese stock tickers by market cap
`plots/`: Contains generated plots and figures
`ovx_stat.py`: Main analysis script, including statistical tests and CAPM model adjustment
`ovx_data.py`: Data gathering and cleaning script

## Prerequisites
* Python 3.x
* Pandas
* yfinance
* BeautifulSoup
* requests
* matplotlib
* os
* csv

## Abstract
Volatility in the oil market has historically been a strong predictor for the movement of the stock market. This paper investigates the relationship between oil price volatility risk and the performance of the Taiwanese stock market. As a proxy for oil price uncertainty, the Crude Oil Volatility Index (OVX) is used. The purpose of this paper is fourfold:

1. To determine if the OVX has an impact on Taiwan’s aggregate stock returns.
2. To evaluate the differential effects of positive and negative OVX movements.
3. To test if oil volatility carries a significant risk premium by adding OVX as a factor into the CAPM model.
4. To analyze exposure to oil price volatility across sectors trading on the Taiwan Stock Exchange.

## Usage
1. Clone the repository.
2. Run ovx_data.py to download and clean the required data.
3. Run ovx_stat.py to execute the analysis and generate plots.

## Contributing
If you would like to contribute to this project, please fork the repository and submit a pull request.

Contact
For more information, please reach out to `patrickwang@berkeley.edu`.