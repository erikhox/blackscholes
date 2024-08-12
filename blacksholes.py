import streamlit as st
import math
from scipy.stats import norm
import seaborn as sn
import matplotlib.pyplot as plt

#defining the functions to create the values for puts and calls
def d1(price, strike, rf, years, vol):
    return (math.log(price/strike)+years*(rf+math.pow(vol, 2)/2))/(vol*math.sqrt(years))

def d2(price, strike, rf, years, vol):
    return d1(price, strike, rf, years, vol) - vol*math.sqrt(years)

def call_value(price, strike, rf, years, vol):
    d1_val = d1(price, strike, rf, years, vol)
    d2_val = d2(price, strike, rf, years, vol)
    return price*norm.cdf(d1_val)-strike*math.exp(-rf*years)*norm.cdf(d2_val)

def put_value(price, strike, rf, years, vol):
    d1_val = d1(price, strike, rf, years, vol)
    d2_val = d2(price, strike, rf, years, vol)
    return strike*math.exp(-rf*years)*norm.cdf(-d2_val)-price*norm.cdf(-d1_val)

#setting up the page layout
st.set_page_config(layout="wide")
st.title("Black-Scholes Pricing Model")
col1, col2 = st.columns(2)

#creating needed variables and adding them to the screen
st.sidebar.title("Black-Scholes Model")
st.sidebar.subheader("created by Erik Hoxhaj")
cap = st.sidebar.number_input("Current Asset Price", value=80.00, step=0.01, min_value=0.0, max_value=9999.00, format="%.2f")
sp = st.sidebar.number_input("Strike Price", value=100.00, step=0.01, min_value=0.0, max_value=9999.00, format="%.2f")
ty = st.sidebar.number_input("Time to Maturity (Years)", value=1.00, step=0.01, min_value=0.0, max_value=9999.00, format="%.2f")
vol = st.sidebar.number_input("Volatility", value=0.20, step=0.01, min_value=0.0, max_value=9999.00, format="%.2f")
rfir = st.sidebar.number_input("Risk-Free Interest rate", value=0.05, step=0.01, min_value=0.0, max_value=9999.00, format="%.2f")
with col1:
    st.subheader("The call value at these values is")
    st.title(f":green-background[{round(call_value(cap, sp, rfir, ty, vol), 2)}]")
with col2:
    st.subheader("The put value at these values is")
    st.title(f":red-background[{round(put_value(cap, sp, rfir, ty, vol), 2)}]")
st.sidebar.write("--------------------------")
st.sidebar.subheader("Heatmap Parameters")
min_vol = st.sidebar.slider("Min volatility", 0.01, 1.00, vol*0.5)
max_vol = st.sidebar.slider("Max Volatility", 0.01, 1.00, vol*1.5)
min_price = st.sidebar.number_input("Min Price", value=cap*0.8, step=0.01, min_value=0.0, max_value=9999.00, format="%.2f")
max_price = st.sidebar.number_input("Max Price", value=cap*1.2, step=0.01, min_value=0.0, max_value=9999.00, format="%.2f")

#the heatmaps are being setup here
st.title("Options Heatmap")
st.subheader("An interactive options heatmap to represent the different values you can get at different spot values and volatility")

col1, col2 = st.columns(2)

rows = [(min_vol + i*(max_vol-min_vol)/9) for i in range(0, 10)]
columns = [(min_price + i*(max_price-min_price)/9) for i in range(0, 10)]
rows_print = [round((min_vol + i*(max_vol-min_vol)/9), 2) for i in range(0, 10)]
columns_print = [round((min_price + i*(max_price-min_price)/9), 2) for i in range(0, 10)]

data_call = []
data_put = []
for i in range(len(rows)):
    data_call_row = []
    data_put_row = []
    for j in range(len(columns)):
        call_val = call_value(columns[j], sp, rfir, ty, rows[i])
        put_val = put_value(columns[j], sp, rfir, ty, rows[i])
        data_call_row.append(call_val)
        data_put_row.append(put_val)
    data_call.append(data_call_row)
    data_put.append(data_put_row)

#outputting the heatmaps to the screen
with col1:  
    st.title("Call Price Map")
    plt.figure(figsize=(10,10))
    sn.heatmap(data=data_call, annot=True, fmt=".2f", cmap="flare", xticklabels=columns_print, yticklabels=rows_print, square=True, cbar_kws={"shrink":0.8})
    plt.xlabel("Spot Price")
    plt.ylabel("Volatility")
    st.pyplot(plt)
    plt.close(None)

with col2:
    st.title("Put Price Map")
    plt.figure(figsize=(10,10))
    sn.heatmap(data=data_put, annot=True, fmt=".2f", cmap="flare",  xticklabels=columns_print, yticklabels=rows_print, square=True, cbar_kws={"shrink":0.8})
    plt.xlabel("Spot Price")
    plt.ylabel("Volatility")
    st.pyplot(plt)
    plt.close(None)