import json
import pandas as pd
import streamlit as st
import requests
import plotly.express as px
import datetime
import plotly.graph_objects as go

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

# set-up all data for one place
def place_set_up(lat, long):
    start = '2005-01-01'
    end = '2023-07-01'

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

    # calculate the moving average
    window_size = 360
    moving_average = data["t_avg"].rolling(window_size).mean()

    # add the moving average to the data variable
    data["moving_average"] = moving_average
    return data

def search_place(place):
    # search place
    # place = 'Zurich'
    url_place = 'https://nominatim.openstreetmap.org/search?q=' + place + '&limit=1&format=json'
    response_place = requests.get(url_place)
    data_place = json.loads(response_place.content)
    name = data_place[0]["display_name"]
    lat = data_place[0]["lat"]
    long = data_place[0]["lon"]
    return name, lat, long

st.set_page_config(page_title="Data you need to see",
                   layout="wide")

col_input, col_result = st.columns([2, 4])

with col_input:
    # get user input
    place = st.text_input("Search for a place.", value="Zurich")
    name, lat, long = search_place(place)
    st.write(name)
    place = pd.DataFrame()
    place["lat"] = 0
    place["long"] = 0
    place.loc[0] = [float(lat), float(long)]
    st.map(place, latitude="lat", longitude="long", zoom=10, size=100)

# get all data for that place
data = place_set_up(lat, long)
# select the data according to user input
data_select = data.loc[data["year"] > 2005]
data_select = data.loc[data["year"] < 2023]

# get the value for the first and last date in the dataset
data_moving_avg = data[data["moving_average"] > 0]
min_val = round(float(data_moving_avg["moving_average"][data_moving_avg["date"] == data_moving_avg["date"].min()]),1)
max_val = round(float(data_moving_avg["moving_average"][data_moving_avg["date"] == data_moving_avg["date"].max()]),1)
delta = round(max_val - min_val,1)

with col_result:
    # show the results
    st.metric(label="Temperature", value=str(max_val)+' °C', delta=str(delta)+' °C')
    st.line_chart(data=data_select, x="date", y=["t_avg", "moving_average"])



