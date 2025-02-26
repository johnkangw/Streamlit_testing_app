"""
This is a testing playground as we consider switching over to Streamlit
From Dash
"""


import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title='Uber NYC data',
    page_icon="🦈",
)

st.sidebar.success("Select a demo above.")

st.title('Uber pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data(
    ttl=60*60*3 # 3 hours time to live
)
def load_data(nrows):
    """
    Loads data
    :param nrows: Number of rows
    :return:
    """
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10k rows of data into the dataframe
data = load_data(10_000)
# Notify the reader that the data was successfully loaded.
data_load_state.text('Done! (using st.cache_data)')

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.dataframe(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

st.subheader('Map of all pickups')
st.map(data)

# hour_to_filter = 17
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)