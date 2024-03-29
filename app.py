import streamlit as str

import pandas as pd
import invest_func
import invest_func_wb

symb_df = pd.read_csv('data/symbols.csv')

user_data_sector = symb_df['Sector'].to_list()
user_data_sector = list(dict.fromkeys(user_data_sector))



str.title('Financial Performance of selected companies.')

option_sector = str.selectbox(
    'Select sector',
    tuple(user_data_sector))


user_data_symbol = symb_df.loc[symb_df['Sector'] == option_sector]
user_data_symbol = user_data_symbol['Symbol'].to_list()



option_symbol = str.multiselect(
   'Select 3 companies tickets in sector: '+ option_sector,
    user_data_symbol)

if len(option_symbol) > 3:
    str.error('Choose only 3 companies!')

btn = str.button('Analyze')

if (btn) and (len(option_symbol) == 3):
    lt = option_symbol

    # Monthly prices for the last year, 5 and 10 years
    pricies_monthly = invest_func.yfin_mprices(lt,10)
     
    chart_data_prices = pricies_monthly.tail(12 * 10)
    str.header('Monthly Prices for the last 10 years')
    str.line_chart(chart_data_prices)

    returns_monthly = invest_func.yfin_mreturns(lt,10)
    chart_data_returns = returns_monthly.tail(12 * 10)
    str.header('Monthly Return for the last 10 years')
    str.line_chart(chart_data_returns)

    str.header('Summary Statistic')
    str.table(invest_func.Summary_Statistic(lt,10))

    str.text('Please wait - calculating the main finance metrics')
    Company_Data = invest_func_wb.fin_data_points_wb(lt)
    str.table(Company_Data.style.apply(invest_func.highlight_thebest_fin))
else:
    if btn:
        str.error('Choose only 3 companies!')

