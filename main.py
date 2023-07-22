import json
import pandas as pd
import streamlit as st
import requests
import plotly.express as px
import datetime

st.set_page_config(page_title="Data you need to see",
                   layout="wide")
def get_data(start, end, lat, long):
    # create url
    url = 'https://archive-api.open-meteo.com/v1/archive?'
    timezone = '&timezone=auto'
    lat = 'latitude=' + lat
    long = '&longitude=' + long
    start = '&start_date=' + start
    end = '&end_date=' + end
    url = url + lat + long + start + end + timezone + '&daily=temperature_2m_max&daily=temperature_2m_min'
    #url = url.replace(" ", "")
    #print(url)
    # get the data
    response = requests.get(url)
    #print(response.content)
    response_data = json.loads(response.content)
    response_df = pd.DataFrame(response_data)
    return response_df

# initialize all variable
start = '1991-01-01'
end = '2023-07-15'
lat = '47.22'
long = '8.33'

# get the data
raw_data = get_data(start, end, lat, long)

data = pd.DataFrame()
data["date"] = raw_data["daily"]["time"]
data["t_max"] = raw_data["daily"]["temperature_2m_max"]
data["t_min"] = raw_data["daily"]["temperature_2m_min"]
data["t_avg"] = (data["t_max"] + data["t_min"]) / 2

# calculate yearly average
# calculate the year for each date
data["date"] = pd.to_datetime(data["date"])
data["year"] = data["date"].dt.year

# calculate the average temperature per year
year_averages = data.groupby("year")["t_avg"].mean()

# add the average yearly temperature to all entries in the data variable
data["t_avg_year"] = data["year"].apply(lambda year: year_averages[year])

# print the year averages
st.write(year_averages)

st.line_chart(data = data, x="date", y=["t_avg", "t_avg_year"])

#print(data)
#fig = px.line(data, x="date", y="t_avg")
#fig.show()
#print(data)

st.dataframe(data)

st.line_chart(data = data, x="date", y="t_avg_year")