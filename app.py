import streamlit as st

import numpy as np
import pandas as pd
import numpy as np
import invest_func
import invest_func_wb


symb_df = pd.read_csv('data/symbols.csv')

user_data_sector = symb_df['Sector'].to_list()
user_data_sector = list(dict.fromkeys(user_data_sector))



st.title('Comparison and analysis of securities of selected companies')

option_sector = st.selectbox(
    'Select sector',
    tuple(user_data_sector))


user_data_symbol = symb_df.loc[symb_df['Sector'] == option_sector]
user_data_symbol = user_data_symbol['Symbol'].to_list()



option_symbol = st.multiselect(
   'Select 3 companies tickets in sector: '+ option_sector,
    user_data_symbol)

if len(option_symbol) > 3:
    st.error('Choose only 3 companies!')


df = pd.DataFrame({
    'first column': list(range(1, 11)),
    'second column': np.arange(10, 101, 10)
})

btn = st.button('Analyze')



if (btn) and (len(option_symbol) == 3):
    lt = option_symbol

    # Monthly prices for the last year, 5 and 10 years
    pricies_monthly = invest_func.yfin_mprices(lt,10)
    chart_data_prices = pricies_monthly.tail(12 * 10)
    st.header('Monthly Prices for the last 10 years')
    st.line_chart(chart_data_prices)

    returns_monthly = invest_func.yfin_mreturns(lt,10)
    chart_data_returns = returns_monthly.tail(12 * 10)
    st.header('Monthly Return for the last 10 years')
    st.line_chart(chart_data_returns)

    st.header('Summary Statistic')
    st.table(invest_func.Summary_Statistic(lt,10))

    st.text('Please wait - calculating the main finance metrics')
    #lt = ["MSFT","AAPL","IBM"]
    Company_Data = invest_func_wb.fin_data_points_wb(lt)
    st.table(Company_Data.style.apply(invest_func.highlight_thebest_fin))
else:
    if btn:
        st.error('Choose only 3 companies!')
