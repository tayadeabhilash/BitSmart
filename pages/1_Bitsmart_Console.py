import streamlit as st
import plotly.graph_objects as go
from keras.models import load_model
import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from datetime import timedelta, datetime
from swing_trade import swing_trade_fn

st.set_page_config(page_title="BitSmart Prediction Console", layout="wide")

todayDate = datetime.today().date()

# Title section
col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    st.write("")
with col2:
    st.title("BitSmart Prediction Console")
with col3:
    st.write("")


# Input section with date picker
col1, col2 = st.columns([1, 2])
with col1:
    today = st.date_input("Assume today's date is:", max_value=todayDate)
with col2:
    if st.button("Predict"):
        st.success("BitSmart has made the following predictions:")

# Load the trained model
model = load_model("model.h5")
stocks = ['BTC-USD']
stock = stocks[0]
stock_data = yf.download(stock, start='2018-01-01', end=today.strftime("%Y-%m-%d"))
ohlc = stock_data[['Open', 'High', 'Low', 'Close']].values
scaler = MinMaxScaler(feature_range=(0,1))
scaled_ohlc = scaler.fit_transform(ohlc)
predicted_prices = []
seq_length = 60
last_seq = ohlc[-seq_length:]
predictions = {}

for _ in range(7):
    last_seq_scaled = scaler.transform(last_seq)
    next_day_scaled = model.predict(np.array([last_seq_scaled]))
    next_day = scaler.inverse_transform(next_day_scaled)[0]
    predicted_prices.append(next_day)
    last_seq = np.append(last_seq[1:], [next_day], axis=0)


# Convert predicted prices to DataFrame with dates
date_range = pd.date_range(start=stock_data.index[-1] + timedelta(days=1), periods=7)
predicted_df = pd.DataFrame(predicted_prices, columns=['Open', 'High', 'Low', 'Close'], index=date_range)
predicted_df.index = predicted_df.index.strftime('%Y-%m-%d') 


# Add the predicted prices to the dictionary
predictions[stock] = predicted_df

# Print the predictions
print(predictions)

# Sample price data (replace with actual data fetching logic)
prices = predicted_df['Close'].tolist()

def create_chart(chart_type, fig_height, fig_width):
    fig = None
    if chart_type == "Candlestick":
        fig = go.Figure(
        data=[go.Candlestick(
            x=predicted_df.index,
            open=predicted_df['Open'],
            high=predicted_df['High'],
            low=predicted_df['Low'],
            close=predicted_df['Close']
            )],
            layout={
                "title": "Predicted Prices for the Next Seven Days (USD)",
                "xaxis_title": "Date",
                "yaxis_title": "Price (USD)",
                "height": fig_height,  
                "width": fig_width,
            }
        )
        
    elif chart_type == "OHLC":
        fig = go.Figure(
            data=[go.Ohlc(
                x=predicted_df.index,
                open=predicted_df['Open'],
                high=predicted_df['High'],
                low=predicted_df['Low'],
                close=predicted_df['Close']
            )],
            layout={
                "title": "Predicted Prices for the Next Seven Days (USD)",
                "xaxis_title": "Date",
                "yaxis_title": "Price (USD)",
                "height": fig_height,  
                "width": fig_width,
            }
        )
    elif chart_type == "Combination":
        fig = go.Figure()

        # Add Candlestick chart
        fig.add_trace(go.Candlestick(
            x=predicted_df.index,
            open=predicted_df['Open'],
            high=predicted_df['High'],
            low=predicted_df['Low'],
            close=predicted_df['Close'],
            name='Candlestick'
        ))

        # Add Line chart
        fig.add_trace(go.Scatter(
            x=predicted_df.index,
            y=predicted_df['Close'],
            mode='lines+markers',
            name='Close Price'
        ))

        fig.update_layout(
            title="Predicted Prices for the Next Seven Days (USD)",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            height=fig_height,
            width=fig_width
        )

    return fig


def data_chart(Data_type, fig_height, fig_width):
    fig = None
    if Data_type == "Close":
            fig = go.Figure(
                data=[go.Scatter(
                    x=predicted_df.index,
                    y=predicted_df['Close'],
                    mode='lines+markers',
                    name='Close',
                    line=dict(color='red')
                )],
                layout={
                    "title": f"Predicted Prices for the Next Seven Days (USD) - {Data_type}",
                    "xaxis_title": "Date",
                    "yaxis_title": f"Price ({Data_type})",
                    "height": fig_height,  
                    "width": fig_width,
                }
            )
    elif Data_type == "High":
            fig = go.Figure(
                data=[go.Scatter(
                    x=predicted_df.index,
                    y=predicted_df['High'],
                    mode='lines+markers',
                    name='High',
                    line=dict(color='red')
                )],
                layout={
                    "title": f"Predicted Prices for the Next Seven Days (USD) - {Data_type}",
                    "xaxis_title": "Date",
                    "yaxis_title": f"Price ({Data_type})",
                    "height": fig_height,  
                    "width": fig_width,
                }
            )
    elif Data_type == "Open":
            fig = go.Figure(
                data=[go.Scatter(
                    x=predicted_df.index,
                    y=predicted_df['Open'],
                    mode='lines+markers',
                    name='Open',
                    line=dict(color='red')
                )],
                layout={
                    "title": f"Predicted Prices for the Next Seven Days (USD) - {Data_type}",
                    "xaxis_title": "Date",
                    "yaxis_title": f"Price ({Data_type})",
                    "height": fig_height,  
                    "width": fig_width,
                }
            ) 
    elif Data_type == "Low":
            fig = go.Figure(
                data=[go.Scatter(
                    x=predicted_df.index,
                    y=predicted_df['Low'],
                    mode='lines+markers',
                    name='Low'
                )],
                layout={
                    "title": f"Predicted Prices for the Next Seven Days (USD) - {Data_type}",
                    "xaxis_title": "Date",
                    "yaxis_title": f"Price ({Data_type})",
                    "height": fig_height,  
                    "width": fig_width,
                }
            )
    return fig

# Display the charts side by side
col1, col2 = st.columns(2)
with col1:
    # Chart type selection
    chart_type = st.selectbox("Select Chart Type",("Candlestick", "OHLC", "Combination"))
    st.plotly_chart(create_chart(chart_type, fig_width=550, fig_height=450))
with col2:
    # Chart type selection
    Data_type = st.selectbox("Select Data Type for Single plot", ("Close", "High", "Open", "Low"))
    st.plotly_chart(data_chart(Data_type, fig_width=550, fig_height=450))

# Display table with predicted values and Predicted Prices (USD) section
col1, col2 = st.columns([2, 1])
with col1:
    st.subheader("Predicted Prices Table")
    st.dataframe(predicted_df)

with col2:
    st.subheader("Predicted Prices (USD)")
    st.write("Highest Price:", max(prices))
    st.write("Lowest Price:", min(prices))
    st.write("Average Closing Price:", sum(prices) / len(prices))

# Trading strategy section
sell, buy = swing_trade_fn(predicted_df, 75, 73000)
col1, col2 = st.columns([1, 1])
with col1:
    st.subheader("Recommended Swing Trading Strategy:")
with col2:
    st.write("")

col1, col2 = st.columns([1, 1])
with col1:
    st.write("Sell All")
    st.write("All In")
with col2:
    sell_date = prices.index(max(prices)) + 1
    st.write(f"Day {sell}")
    st.write(f"Day {buy}")

# Disclaimer section

st.write("---")
st.write(
    'Note: This is a sample prediction and may not be accurate. Please do your own research '
    'before making any investment decisions.')
