import streamlit as str

import pandas as pd


#def test_stremlit(tickets_lt):
    #l = len(tickets_lt)
    #df = pd.DataFrame(tickets_lt)
    #return df

symb_df = pd.read_csv('data/symbols.csv')

user_data_sector = symb_df['Sector'].to_list()
user_data_sector = list(dict.fromkeys(user_data_sector))



str.title('Comparison and analysis of securities of selected companies')

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

#check
if btn:
    str.write("click")
lt = ["MSFT","AAPL"]
str.header('Monthly Prices for the last 10 years!')
df_test = pd.DataFrame(lt)
str.write(df_test)
str.dataframe(df_test)
