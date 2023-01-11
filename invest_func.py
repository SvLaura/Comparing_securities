
#import yahoo_fin as yfin
import yahoo_fin.stock_info as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# for Conditional Formatting
import dash
from dash import dash_table
from dash import html
import colorlover
from jupyter_dash import JupyterDash
import csv

# Functions

def mf_iserror(func, *args, **kw):
    exception = kw.pop('exception', Exception)
    try:
        func(*args, **kw)
        return func(*args, **kw)
    except exception:
        return '' 
        
# Finance data  
def fin_data_points(tickets):    
    '''
    Computes finance data for the given list of assets (tickets)
    '''
    
    #tickets = ["MSFT","GM"]#,"BMW.DE","AAPL","NFLX","IBM"]

    def company_finance_fn(tbl_name,column_name):
        totalAssets_tbl = tbl_name.loc[column_name]
        totalAssets_maxdt = totalAssets_tbl.index.max()
        return totalAssets_tbl["endDate" == totalAssets_maxdt]  
    
    def txt_to_num(text, bad_data_val = 0):
        d = {
            'K': 1000,
            'k': 1000,
            'M': 1000000,
            'B': 1000000000
        }
        if not isinstance(text, str):
            return bad_data_val

        elif text[-1] in d:
            # separate out the K, M, or B
            num, magnitude = text[:-1], text[-1]
            return int(float(num) * d[magnitude])
        else:
            return text

    #create tbl:
    Company_Data = pd.DataFrame(columns = ['P/B','P/E','D/E','ROE','ROA',
                                       'NetProfit','GrossProfit','EBIT',
                                       'ProfitMargin', 'ForwardDividendYeild',
                                       'Name','Industry','Sector','Country', 'Currency'], index = tickets) 

  
    for i in range(len(tickets)):
        company = tickets[i]
        
        #get data from Yahoo Finance:
        info = mf_iserror(st.get_company_info, company)
        #forecast = st.get_analysts_info(company)
        balance_tbl = st.get_balance_sheet(company)
        income_tbl = st.get_income_statement(company)
        stats_tbl = st.get_stats(company)
        fins = st.get_financials(company, yearly = True, quarterly = False)
        fin_tbl = fins['yearly_income_statement']
        qd = st.get_quote_data(company)
        
        Company_Capitalization = qd['marketCap']
        Company_Assets = company_finance_fn(balance_tbl,"totalAssets")
        Company_Liabilities = company_finance_fn(balance_tbl,"totalLiab")
        Company_Equity =  Company_Assets - Company_Liabilities
        Company_NetProfit = company_finance_fn(income_tbl,"totalRevenue") 
        
        if Company_Equity != 0:
            PB = Company_Capitalization/abs(Company_Equity)
            Company_Data['P/B'].loc[company] = round(PB,4)
        if Company_NetProfit != 0:
            PE = Company_Capitalization/Company_NetProfit
            Company_Data['P/E'].loc[company] = round(PE,4)
                
        DE = Company_Liabilities/Company_Equity
              
        GrossProfit = company_finance_fn(income_tbl,"grossProfit")
        Ebit = company_finance_fn(income_tbl,"ebit")
        
        #find data in stats_tbl: 
        def is_stat_dt(k,param):
            return stats_tbl.iloc[k,0] == param       
        i = 0
        while i < len(stats_tbl):
            if is_stat_dt(i,'Return on Assets (ttm)'):
                ROA = stats_tbl.iloc[i,1]
            if is_stat_dt(i,'Return on Equity (ttm)'):
                ROE = stats_tbl.iloc[i,1]
            if is_stat_dt(i,'Profit Margin'):
                ProfitMargin = stats_tbl.iloc[i,1]
            if is_stat_dt(i,'Forward Annual Dividend Yield 4'):
                ForwardDividendYeild = stats_tbl.iloc[i,1]
            i = i + 1
    
        
        #fill tbl:
        Company_Data['D/E'].loc[company] = round(DE,2)
        Company_Data['ROE'].loc[company] = ROE
        Company_Data['ROA'].loc[company] = ROA
                      
        Company_Data['NetProfit'].loc[company] = txt_to_num(str(Company_NetProfit))
        Company_Data['GrossProfit'].loc[company] = txt_to_num(str(GrossProfit))
        Company_Data['EBIT'].loc[company] = txt_to_num(str(Ebit))
        Company_Data['ProfitMargin'].loc[company] = txt_to_num(str(ProfitMargin))
        Company_Data['ForwardDividendYeild'].loc[company] = ForwardDividendYeild
        
        Company_Data['Name'].loc[company] = qd['longName']
        if len(info) > 0 :
            Company_Data['Industry'].loc[company] = info.loc['industry'].Value
            Company_Data['Sector'].loc[company] = info.loc['sector'].Value  
            Company_Data['Country'].loc[company] = info.loc['country'].Value
        Company_Data['Currency'].loc[company] = qd['currency']
    return Company_Data
    
def highlight_thebest_fin(data):
    '''
    highlight the minimum in columns in "P/B","P/E","D/E"
    highlight the maximum in other columns
    '''
    color='green'
    min_v = ["P/B","P/E","D/E"]
    attr = 'background-color: {}'.format(color)
    #remove % and cast to float
    data = data.replace('%','', regex=True).astype(float)
    if data.ndim == 1:  # Series from .apply(axis=0) or axis=1
        if data.name not in min_v:
            is_max = data == data.max()
            return [attr if v else '' for v in is_max]
        else:
            is_min = data == data.min()
            return [attr if v else '' for v in is_min]
    else:  # from .apply(axis=None)
        is_max = data == data.max().max()
        return pd.DataFrame(np.where(is_max, attr, ''),
                            index = data.index, columns = data.columns)

#Fin_Data = Company_Data.loc[:,'P/B':'ForwardDividendYeild']
    #return Company_Data.style.apply(highlight_thebest_fin)


# Prices daily/weekly/ monthly price data from yfninace for the list of assets (as_lt)  - period = n_years
def yfin_dprices(lt, n_years = 5, n_interval = "1d"):
    from dateutil.relativedelta import relativedelta
    import datetime
    dt = datetime.date.today()    
    dt_minus_nyears = (dt - relativedelta(years = n_years)).strftime('%Y-%m-%d')
    dt = dt.strftime('%Y-%m-%d')

    prices = pd.DataFrame(columns=lt)

    for l in lt:
        #prices[l] = yf.download(l,dt_minus_nyears,dt)['Adj Close']         
        #prices from yahoo_fin:
        prices[l] = st.get_data(l, start_date = dt_minus_nyears, end_date = dt, interval = n_interval)['adjclose']
    return prices


def yfin_wkprices(lt, n_years = 5 ): 
    #return yfin_dprices(lt, n_years, "1wk")
    return yfin_dprices(lt, n_years).resample('W').apply(lambda x: x[-1])
    

def yfin_mprices(lt, n_years = 5 ):
    #return yfin_dprices(lt, n_years, "1mo")
    return yfin_dprices(lt, n_years).resample('BM').apply(lambda x: x[-1])

# Returns daily/weekly/ monthly price data from yfninace for the list of assets (as_lt)
def yfin_dreturns(lt, n_years = 5):
    prices_daily = yfin_dprices(lt, n_years)
    returns_daily= prices_daily.pct_change()
    returns_daily = returns_daily.dropna() #delete Na   
    return returns_daily

def yfin_wkreturns(lt, n_years = 5 ):
    prices_weekly = yfin_wkprices(lt,n_years)
    returns_weekly = prices_weekly.pct_change()   
    returns_weekly = returns_weekly.dropna() #delete Na
    #returns_daily = returns_daily.fillna(0, inplace=True)
    return returns_weekly 

def yfin_wkreturns_TB(lt, n_years = 5 ):
    prices_weekly = yfin_dprices(lt, n_years, "1wk")
    returns_weekly = prices_weekly.pct_change()    
    returns_weekly = returns_weekly.dropna() #delete Na
    return returns_weekly 

def yfin_mreturns(lt, n_years = 5):
    prices_monthly = yfin_mprices(lt, n_years)
    returns_monthly = prices_monthly.pct_change()
    returns_monthly = returns_monthly.dropna() #delete Na   
    returns_monthly.index = pd.to_datetime(returns_monthly.index, format="%Y%m").to_period('M')   
    return returns_monthly
    
    
# Risk Functions - annualizing returns, volatility (std dev), sharpe ratio coef, max drawdown
def annualize_rets(r, periods_per_year = 12):
    compounded_growth = (1 + r).prod()
    n_periods = r.shape[0]
    return compounded_growth**(periods_per_year/n_periods) - 1 #return (x+1)**Freq-1

def annualize_vol(r, periods_per_year = 12):
    return r.std()*(periods_per_year**0.5) #x*np.sqrt(Freq)

def RiskFree_wk(n_years):
    """
    take 13 Week Treasury Bill  as a risk-free rate - to calculate Sharpe ratio
    ^IRX from yfinance
    """
    TBill_wk = yfin_wkreturns_TB(lt = ["^IRX"],n_years = n_years)

    RiskFree_df = pd.DataFrame(columns = ['RET'], index = TBill_wk.index) 
    RiskFree_df['RET'] = (TBill_wk['^IRX'].values/100 + 1) ** (1 / 52) - 1 #weekly frequency = 52 per year


    RiskFree_df_weekly = (RiskFree_df['RET'] + 1).resample('W').prod() - 1 # to the same weekly frequency = 52 
    TBill_wk = pd.DataFrame(columns = ['T-Bill'], index = RiskFree_df_weekly.index)  #create a new dataframe 
    TBill_wk['T-Bill'] = RiskFree_df_weekly

    #ind = (TBill.index >= RiskFree_df_weekly.index[[0]][0])*(TBill.index <= RiskFree_df_weekly.index[[-1]][0])
    #TBill = TBill[ind] #keep the same start and end date as the stock returns data    
    return TBill_wk

def ann_sharpe_ratio(r, riskfree_rate, periods_per_year = 52): 
    n = len(r)
    ret_expected = np.sum(r - riskfree_rate)/n
    ret_avg = np.sum(r)/n
    std_dev = np.sqrt( np.sum( (r - ret_avg)**2 ) / n )
    ann_ret_expected = (ret_expected + 1)**periods_per_year - 1
    ann_std_dev = std_dev * np.sqrt(periods_per_year)
    return ann_ret_expected/ann_std_dev


def max_drawd(r):
    wealth = (r + 1).cumprod()
    cummax = wealth.cummax() 
    drawdown = wealth/cummax - 1 
    return drawdown.min()

def Summary_Statistic(lt,period = 10):
    returns_weekly = yfin_wkreturns(lt,period)
    TBill_wk = RiskFree_wk(period)

    data = returns_weekly
    SumStat = pd.DataFrame(index = data.columns)

    SumStat['Annualize Returns(,%)'] = np.round( annualize_rets(data,52)*100, 2)
    SumStat['Annualize Volatility(,%)'] = np.round( annualize_vol(data,52)*100, 2)
    SumStat['Annual Sharpe Ratio'] = np.round(data.apply(ann_sharpe_ratio, riskfree_rate = TBill_wk['T-Bill'], periods_per_year = 52), 2)
    SumStat['Max Drawdown(%)'] = np.round(data.apply(max_drawd)*100, 2)

    max_rt = SumStat['Annualize Returns(,%)'].max()
    pr_rt = max_rt * 0.5
    SumStat['Rating Returns'] = SumStat['Annualize Returns(,%)'].apply(lambda x:
      '⭐⭐⭐' if x == max_rt else (   
       '⭐⭐' if x > pr_rt else (
      '⭐' if x > 0 else ''  #the first place
    )))

    SumStat['SR rating'] = SumStat['Annual Sharpe Ratio'].apply(lambda x: '🔥' if x == SumStat['Annual Sharpe Ratio'].max() else '')
    return SumStat.sort_values('Annual Sharpe Ratio')
