import os
import pickle
import streamlit as st
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import time

# Page config
st.set_page_config(page_title='Forecast', page_icon='📉', layout="centered", initial_sidebar_state="auto", menu_items=None)

if 'measles_button' not in st.session_state:
    st.session_state.measles_button = False
if 'p_button' not in st.session_state:
    st.session_state.p_button = False
# On-click
def measles_button():
    st.session_state.measles_button = True
def p_button():
    st.session_state.p_button = True

# Title
st.title('📉 Communicable Disease Forecast')
with st.expander('❤️ AT A GLANCE'):
    st.write("""PULSO Predict also includes time series forecasting capabilities to predict communicable disease trends such as measles and pertussis, enabling proactive resource allocation and outbreak response. With Disease Predict, stay ahead of disease trends and take steps to safeguard public health.""")
st.write('\n')

# Tab 1: Measles
col1, col2 = st.columns(2)
start_m = col1.selectbox('Choose starting date', ['February 17','March 17','April 17'], key='start_m')
end_m = col2.selectbox('Choose ending date', ['February 17','March 17','April 17'], key='end_m', index=1)

tab1, tab2 = st.tabs(["Measles", "Pertussis"])
with tab1:
    st.button('Begin Measles analysis', on_click=measles_button, type='primary')

    if st.session_state.measles_button:
        with st.spinner('Fetching data...'):
            time.sleep(1)
        st.toast('Analysis complete!', icon='✅')
        st.session_state.measles_date = [start_m, end_m]
        st.header(f'Analysis from {st.session_state.measles_date[0]} to {st.session_state.measles_date[-1]}')

        measles_dataset = pd.read_csv('datasets/measles_cases.csv') 
        measles_df = pd.read_csv('datasets/measles_cases.csv')

        # Convert DateTime to datetime type
        measles_df['Date'] = pd.to_datetime(measles_df['Date'])

        # Extract date (year-month-day) from DateTime
        measles_df['Date'] = measles_df['Date'].dt.date

        # Group by Date and count Outcomes
        measles_grouped_df = measles_df.groupby('Date')['Outcome'].value_counts().unstack(fill_value=0)

        # Rename columns for clarity
        measles_grouped_df.columns = ['Without Measles', 'With Measles']

        # Reset index to make 'Date' a column again
        measles_grouped_df.reset_index(inplace=True)

        # Convert 'Date' column to datetime type
        measles_grouped_df['Date'] = pd.to_datetime(measles_grouped_df['Date'])

        # Set 'Date' as index
        measles_grouped_df.set_index('Date', inplace=True)

        # Resample by week and sum the counts
        weekly_df = measles_grouped_df.resample('W').sum()

        # Reset index to make 'Date' a column again
        weekly_df.reset_index(inplace=True)

        measles = pd.DataFrame()

        weekly_df['Year'] = weekly_df['Date'].apply(lambda x: str(x)[:4])
        weekly_df['Month'] = weekly_df['Date'].apply(lambda x: str(x)[5:7])
        weekly_df['Day'] = weekly_df['Date'].apply(lambda x: str(x)[8:])
        measles['ds'] = pd.DatetimeIndex(weekly_df['Year']+'-'+ weekly_df['Month']+'-'+ weekly_df['Day'])
        measles['y'] = weekly_df['With Measles']
        m = Prophet(interval_width=0.95, daily_seasonality=True)
        model = m.fit(measles)

        measles_future = m.make_future_dataframe(periods=90,freq='D')
        measles_forecast = m.predict(measles_future)

        measles_fig = m.plot(measles_forecast)
        ax = measles_fig.gca()  # Get the current axes
        ax.set_xlabel('Date')  # Set the x-axis label
        ax.set_ylabel('Number of People with Measles')  # Set the y-axis label

        with st.container(border=True):
            st.caption(body = '3-month Prediction 🗓️')
            st.pyplot(measles_fig)
            
            measles_plt = m.plot_components(measles_forecast)

            # Create a figure with two subplots side by side
            fig, axes = plt.subplots(1, 2, figsize=(14, 7))

            # Copy the first graph from plt2 to the new axes
            for line in measles_plt.axes[0].lines:
                axes[0].plot(line.get_xdata(), line.get_ydata())
            axes[0].set_title('General Trend')
            axes[0].set_xlabel('Date')
            axes[0].set_ylabel('Trend')
            axes[0].tick_params(axis='x', rotation=45)  # Rotate x-axis labels

            # Copy the second graph from plt2 to the new axes
            for line in measles_plt.axes[1].lines:
                axes[1].plot(line.get_xdata(), line.get_ydata())
            axes[1].set_title('Daily Trend')
            axes[1].set_xlabel('Time')
            axes[1].set_ylabel('Trend')
            axes[1].tick_params(axis='x', rotation=45)  # Rotate x-axis labels

            # Fix y-axis format for "Hour of day"
            import matplotlib.dates as mdates
            axes[1].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        with st.container(border=True):
            st.caption(body = 'Trend 📈')
            st.pyplot(fig)


# Tab 2: Pertussis
with tab2:

    col1, col2 = st.columns(2)
    st.button('Begin Pertussis analysis', on_click=p_button,type='primary')

    if st.session_state.p_button:
        with st.spinner('Fetching data...'):
            time.sleep(1)
        st.toast('Analysis complete!', icon='✅')
        st.session_state.p_date = [start_m, end_m]
        st.header(f'Analysis from {st.session_state.p_date[0]} to {st.session_state.p_date[-1]}')

        pertussis_dataset = pd.read_csv('datasets/pertussis_cases.csv') 
        pertussis_df = pd.read_csv('datasets/pertussis_cases.csv')

        # Convert DateTime to datetime type
        pertussis_df['Date'] = pd.to_datetime(pertussis_df['Date'])

        # Extract date (year-month-day) from DateTime
        pertussis_df['Date'] = pertussis_df['Date'].dt.date

        # Group by Date and count Outcomes
        pertussis_grouped_df = pertussis_df.groupby('Date')['Outcome'].value_counts().unstack(fill_value=0)

        # Rename columns for clarity
        pertussis_grouped_df.columns = ['Without Pertussis', 'With Pertussis']

        # Reset index to make 'Date' a column again
        pertussis_grouped_df.reset_index(inplace=True)

        # Convert 'Date' column to datetime type
        pertussis_grouped_df['Date'] = pd.to_datetime(pertussis_grouped_df['Date'])

        # Set 'Date' as index
        pertussis_grouped_df.set_index('Date', inplace=True)

        # Resample by week and sum the counts
        weekly_df = pertussis_grouped_df.resample('W').sum()

        # Reset index to make 'Date' a column again
        weekly_df.reset_index(inplace=True)

        pertussis = pd.DataFrame()

        weekly_df['Year'] = weekly_df['Date'].apply(lambda x: str(x)[:4])
        weekly_df['Month'] = weekly_df['Date'].apply(lambda x: str(x)[5:7])
        weekly_df['Day'] = weekly_df['Date'].apply(lambda x: str(x)[8:])
        pertussis['ds'] = pd.DatetimeIndex(weekly_df['Year']+'-'+ weekly_df['Month']+'-'+ weekly_df['Day'])
        pertussis['y'] = weekly_df['With Pertussis']
        m = Prophet(interval_width=0.95, daily_seasonality=True)
        model = m.fit(pertussis)

        pertussis_future = m.make_future_dataframe(periods=90,freq='D')
        pertussis_forecast = m.predict(pertussis_future)

        pertussis_fig = m.plot(pertussis_forecast)
        ax = pertussis_fig.gca()  # Get the current axes
        ax.set_xlabel('Date')  # Set the x-axis label
        ax.set_ylabel('Number of People with Pertussis')  # Set the y-axis label

        with st.container(border=True):
            st.caption(body = '3-month Prediction 🗓️')
            st.pyplot(pertussis_fig)
            
            pertussis_plt = m.plot_components(pertussis_forecast)

            # Create a figure with two subplots side by side
            fig, axes = plt.subplots(1, 2, figsize=(14, 7))

            # Copy the first graph from plt2 to the new axes
            for line in pertussis_plt.axes[0].lines:
                axes[0].plot(line.get_xdata(), line.get_ydata())
            axes[0].set_title('General Trend')
            axes[0].set_xlabel('Date')
            axes[0].set_ylabel('Trend')
            axes[0].tick_params(axis='x', rotation=45)  # Rotate x-axis labels

            # Copy the second graph from plt2 to the new axes
            for line in pertussis_plt.axes[1].lines:
                axes[1].plot(line.get_xdata(), line.get_ydata())
            axes[1].set_title('Daily Trend')
            axes[1].set_xlabel('Time')
            axes[1].set_ylabel('Trend')
            axes[1].tick_params(axis='x', rotation=45)  # Rotate x-axis labels

            # Fix y-axis format for "Hour of day"
            import matplotlib.dates as mdates
            axes[1].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        with st.container(border=True):
            st.caption(body = 'Trend 📈')
            st.pyplot(fig)