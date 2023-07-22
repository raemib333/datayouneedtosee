import json

import pandas as pd
import streamlit as st
import requests


def get_data(start, end, lat, long):
    # create url
    url = 'https://archive-api.open-meteo.com/v1/archive?'
    timezone = 'auto'
    lat = 'latitude=' + lat
    long = '&longitude=' + long
    start = '&' + start
    end = '&' + end
    url = url + lat + long + start + end + timezone + 'daily=temperature_2m_max&daily=temperature_2m_mi'

    # get the data
    response = requests.get(url)
    # print(response.content)
    response_data = json.loads(response.content)
    response_df = pd.DataFrame(response_data)
    return (response_df)

'https://archive-api.open-meteo.com/v1/archive?latitude=47.222&longitude=8.33&start_date=2023-07-01&end_date=2023-07-16&hourly=temperature_2m'

url = 'https://archive-api.open-meteo.com/v1/archive?latitude=47.222&longitude=8.33&start_date=2023-07-01&end_date=2023-07-16&timezone=auto&daily=temperature_2m_max&daily=temperature_2m_min'
response = requests.get(url)
#print(response.content)
response_data = json.loads(response.content)
response_df = pd.DataFrame(response_data )

data = pd.DataFrame()
data["date"] = response_df["daily"]["time"]
data["t_max"] = response_df["daily"]["temperature_2m_max"]
data["t_min"] = response_df["daily"]["temperature_2m_min"]
data["t_avg"] = (data["t_max"] + data["t_min"]) / 2

print(data)

'''
st.set_page_config(page_title="Hotel Data",
                   layout="wide")


df1 = pd.read_excel(
    io="Data_1.xlsx",
    engine="openpyxl",
)

print(df1)

st.dataframe(df1)
'''