import streamlit as st
import plotly.graph_objects as go
from keras.models import load_model
import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from datetime import timedelta, datetime

st.set_page_config(page_title="BitSmart Prediction Console", layout="wide")

# Custom CSS for styling
st.write("""
<style>
body {
    font-family: 'Helvetica Neue', sans-serif;
    background-color: #f0f2f5;
}
.title {
    color: #343a40;
    text-align: center;
}
.subheader {
    font-weight: bold;
    color: #343a40;
}
.data-point {
    margin-bottom: 5px;
}
.disclaimer {
    font-size: 0.8rem;
    color: #999;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)
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
col1, col2 = st.columns([2, 1])
with col1:
    today = st.date_input("Assume today's date is:", max_value=todayDate)
with col2:
    if st.button("Predict"):
        st.success("BitSmart has made the following predictions:")

print(today)
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
date_range = pd.date_range(start=stock_data.index[-1] + timedelta(days=1), periods=7, freq='B')
predicted_df = pd.DataFrame(predicted_prices, columns=['Open', 'High', 'Low', 'Close'], index=date_range)

# Add the predicted prices to the dictionary
predictions[stock] = predicted_df

# Print the predictions
print(predictions)
# Sample price data (replace with actual data fetching logic)
prices = predicted_df['Close'].tolist()

# Chart with Plotly

fig = go.Figure(
    data=[go.Scatter(x=[f"Day {i + 1}" for i in range(7)], y=prices)],
    layout={
        "title": "Predicted Prices for the Next Seven Days (USD)",
        "xaxis_title": "Day",
        "yaxis_title": "Price (USD)",
    },
)
st.plotly_chart(fig)

# Predicted prices section
col1, col2 = st.columns([1, 1])
with col1:
    st.subheader("Predicted Prices (USD)")
with col2:
    st.write("")

col1, col2 = st.columns([1, 1])
with col1:
    st.write("Highest Price")
    st.write("Lowest Price")
    st.write("Average Closing Price")
with col2:
    st.write(max(prices))
    st.write(min(prices))
    st.write(sum(prices) / len(prices))

# Trading strategy section
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
    # Replace with actual recommendation logic (e.g., based on price trend)
    sell_date = prices.index(max(prices)) + 1
    st.write(f"Day {sell_date}")
    st.write("NA")

# Disclaimer section
st.write("---")
st.write(
    'Note: This is a sample prediction and may not be accurate. Please do your own research '
    'before making any investment decisions.')
