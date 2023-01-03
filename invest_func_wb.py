import lxml
from lxml import html
import requests
import numpy as np
import pandas as pd

def digit_abbr(digit):
    m = {'K': 3, 'M': 6, 'B': 9, 'T': 12}
    abbr = digit[-1]
    if abbr in m:
        return int(float(digit[:-1]) * 10 ** m[abbr])
    else:
        return float(digit)

def page_to_df(url, page_type):
    '''
    from the given url (yahoo website - pages statistic, finance)
    return data (df)
    '''
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'close',
        'DNT': '1', # Do Not Track Request Header
        'Pragma': 'no-cache',
        'Referrer': 'https://google.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    }

    page = requests.get(url, headers=headers)
    tree = html.fromstring(page.content)
    tree.xpath("//h1/text()")

    if page_type != 'statistic':
        table_rows = tree.xpath("//div[contains(@class, 'D(tbr)')]")
        assert len(table_rows) > 0
        parsed_rows = []
        for table_row in table_rows:
            parsed_row = []
            el = table_row.xpath("./div")
            none_count = 0
            for rs in el:
                try:
                    (text,) = rs.xpath('.//span/text()[1]')
                    parsed_row.append(text)
                except ValueError:
                    parsed_row.append(np.NaN)
                    none_count += 1
            if (none_count < 4):
                parsed_rows.append(parsed_row)

    if page_type == 'statistic':
        table_rows = tree.xpath("//td[contains(@class, 'Fw(500) Ta(end) Pstart(10px) Miw(60px)')]")
        assert len(table_rows) > 0
        parsed_rows = []
        for table_row in table_rows:
            parsed_rows.append(table_row.text)
    df = pd.DataFrame(parsed_rows)
    return df



# Finance data
def fin_data_points_wb(tickets):
    '''
    Computes finance data for the given list of assets (tickets)
    '''
    #tickets = ["MSFT","GM"]#,"BMW.DE","AAPL","NFLX","IBM"]

    #create tbl:
    Company_Data = pd.DataFrame(columns = ['P/B','P/E','ROE','ROA',
                                       'NetProfit','GrossProfit','EBIT',
                                       'ProfitMargin', 'ForwardDividendYeild',
                                        'week52_high','week52_low'], index = tickets)


    for i in range(len(tickets)):
        company = tickets[i]

        #staistic data:
        page_type = 'statistic'
        url = 'https://ca.finance.yahoo.com/quote/'+ company + '/key-statistics?p=' + company
        df = page_to_df(url, page_type)

        Company_Capitalization_abbr = df.iloc[0,0]
        Company_Capitalization = digit_abbr(Company_Capitalization_abbr)
        ROA = df.iloc[42,0]
        ROE = df.iloc[43,0]
        ProfitMargin = df.iloc[40,0]
        ForwardDividendYeild = df.iloc[29,0]#Forward Annual Dividend Yield
        week52_high = df.iloc[12,0]
        week52_low = df.iloc[13,0]
        Ebit_abbr = df.iloc[48,0]
        Ebit = digit_abbr(Ebit_abbr)

        #finance sheet
        page_type = 'finance'
        url =  'https://ca.finance.yahoo.com/quote/'+ company + '/financials?p=' + company
        df = page_to_df(url, page_type)

        Company_NetProfit_abbr = df.iloc[1,1] #Total Revenue
        Company_NetProfit = float(Company_NetProfit_abbr.replace(',',''))
        GrossProfit_abbr = df.iloc[3,1]
        GrossProfit = GrossProfit_abbr.replace(',','')

        #balance sheet
        page_type = 'balance'
        url = 'https://finance.yahoo.com/quote/' + company + '/balance-sheet?p=' + company
        df = page_to_df(url, page_type)

        Company_Assets_abbr = df.iloc[7,1]
        Company_Assets = Company_Assets_abbr.replace(',','')
        Company_Liabilities_abbr = df.iloc[2,1] #Total Liabilities Net Minority Interest
        Company_Liabilities = Company_Liabilities_abbr.replace(',','')

        #fill tbl:
        Company_Equity =  float(Company_Assets) - float(Company_Liabilities)
        PB = Company_Capitalization/abs(Company_Equity)
        PE = Company_Capitalization/Company_NetProfit
        Company_Data['P/B'].loc[company] = round(PB,4)
        Company_Data['P/E'].loc[company] = round(PE,4)
        Company_Data['ROE'].loc[company] = ROE
        Company_Data['ROA'].loc[company] = ROA

        Company_Data['NetProfit'].loc[company] = Company_NetProfit
        Company_Data['GrossProfit'].loc[company] = GrossProfit
        Company_Data['EBIT'].loc[company] = Ebit
        Company_Data['ProfitMargin'].loc[company] = ProfitMargin
        Company_Data['ForwardDividendYeild'].loc[company] = ForwardDividendYeild
        Company_Data['week52_high'].loc[company] = week52_high
        Company_Data['week52_low'].loc[company] = week52_low

    return Company_Data
