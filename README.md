# Comparing_securities

## Business Objective
The analysis compares companies by financial performance based on Yahoo's historical data.
As a result of financial and technical analysis, recommendations are automatically generated on which of the 3 given market stock is the best. The Sharpe Ratio was chosen as the main indicator of the best solution because it is a risk-adjusted measure of return.

## Data  
<ul>The dataset was gathered from 3 different data sourses:
  <li> python3 package - yahoo_fin</li>
  <li> web pages -  the basic financial information was web scrapping from the yahoo finance website https://ca.finance.yahoo.com/</li>
  <li> csv file - data was retrived from the file  - data/symbols.csv. </li>
 </ul>
 
 ## Repository overview
 The directory structure:

 * [data](./data)
   * [symbols.scv](./data/symbols.scv)  #the file contains stock ticker symbols, name, vectors. 489 rows
 * [app.py](./app.py)    #main file for run in Streamlit
 * [Invest_yahoo_fin.ipynb](./Invest_yahoo_fin.ipynb)   #notebook
 * [Invest_yfinance_data.ipynb](./Invest_yfinance_data.ipynb)   #notebook
 * [invest_func.py](./invest_func.py)  #functions - yahoo_fin
 * [invest_func_wb.py](./invest_func_wb.py)   #functions - web scrapping
 * [README.md](./README.md)
 * [equirements.txt](./equirements.txt)    #a list of package names


## Visualisation
The interactive report has been deployed in the Streamlit.You can access here:

https://svlaura-comparing-securities-app-u9jf8v.streamlit.app/

## Vocabulary
**SR** -  Sharpe ratio. It is a way to measure the performance of an investment by taking risk into account.
The calculation was based on historical returns.
<p>Sharpe Ratio = (Rp – Rf) / Standard deviation</p>
Rp is the expected return (or actual return for historical calculations) on the asset or the portfolio being measured.
Rf is a risk-free rate - U.S. Treasury bill. Used to calculate SR
Standard deviation is a measure of risk based on volatility. The lower the standard deviation, the less risk and the higher the Sharpe ratio, all else being equal. Conversely, the higher the standard deviation, the more risk and the lower the Sharpe ratio.

**ROI** -Returns. It is an approximate measure of an investment's profitability.
A positive return means a profit has been made on the investment. A negative return means that there has been a loss on the investment.

**P/B** - Price to Book ratio. The P/B ratio is used to compare the market value of a company with its book value. It seeks the value that the stock market places on a company’s stock relative to the book value of the company. A company with sound financial health will trade for more than its book value since investors will consider the company’s future growth while pricing the stocks.

**P/E** - Price to Earnings ratio. The P/E ratio indicates how much investors are willing to pay for the earnings of a company. A higher P/E value could mean an overvalued stock. Or, it could imply that the market is expecting the company to perform extremely well over time. On the other hand, a low P/E value is seen as unfavorable by the market.

**ROE** - Return on Equity. It measures how effectively a company uses its assets for producing earnings. A high ROE implies that a company squeezes out greater profits with available assets. 

**ROA** - Return on assets. It s an indicator of how profitable a company is relative to its assets or the resources it owns or controls. Investors can use ROA to find good stock opportunities because the percentage shows how efficient a company is at using its assets to generate profits.
to determine how effectively a company is using its resources to make a profit.

**NetProfit** It represents the financial standing of a company after all its expenses have been paid off from its total revenue.

**GrossProfit** The gross profit of a company is the total sales of the firm minus the total cost of the goods sold.

**EBIT** - Earnings before interest and taxes. It is an indicator of a company's profitability.

**ProfitMargin** It represents what percentage of sales has turned into profits. profit margin indicates how many cents of profit has been generated for each dollar of sale.

**ForwardDividendYeild** It is used to predict how much a company will pay in dividends in a future period.

**week52_high** It is the highest price in 52 week period.

**week52_low** It is the  lowest price in 52 week period.
