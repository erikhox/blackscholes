import streamlit as st
from scipy.stats import norm
import seaborn as sn
import matplotlib.pyplot as plt
import numpy as np

def d1(price, strike, rf, years, volatility):
    '''returns the d1 of the Black-Scholes formula'''
    return (np.log(price/strike)+years*(rf+np.pow(volatility, 2)/2))/(volatility*np.sqrt(years))

def d2(price, strike, rf, years, volatility):
    '''returns the d2 of the Black-Scholes formula'''
    return d1(price, strike, rf, years, volatility) - volatility*np.sqrt(years)

def call_value(price, strike, rf, years, volatility):
    '''returns the call premium cost using the Black-Scholes formula'''
    d1_val = d1(price, strike, rf, years, volatility)
    d2_val = d2(price, strike, rf, years, volatility)
    return price*norm.cdf(d1_val)-strike*np.exp(-rf*years)*norm.cdf(d2_val)

def put_value(price, strike, rf, years, volatility):
    '''returns the put premium cost using the Black-Scholes formula'''
    d1_val = d1(price, strike, rf, years, volatility)
    d2_val = d2(price, strike, rf, years, volatility)
    return strike*np.exp(-rf*years)*norm.cdf(-d2_val)-price*norm.cdf(-d1_val)

def heat_map(col, row, title):
    '''forms the asset price vs volatility heat map'''
    st.title(f"{title} Price Map")
    plt.figure(figsize=(10,10))
    sn.heatmap(data=data_call, annot=True, fmt=".2f", cmap="flare", xticklabels=col, yticklabels=row, square=True, cbar_kws={"shrink":0.8})
    plt.xlabel("Asset Price")
    plt.ylabel("volatility")
    st.pyplot(plt)
    plt.close(None)

def print_value(price, strike, rf, years, volatility):
    '''prints the call and put values to the screen'''
    with col1:
        st.subheader("The call value at these values is")
        st.title(f":green-background[{round(call_value(price, strike, rf, years, volatility), 2)}]")

    with col2:
        st.subheader("The put value at these values is")
        st.title(f":red-background[{round(put_value(price, strike, rf, years, volatility), 2)}]")

def delta(option_type, price, strike, rf, years, volatility):
    '''returns the delta of the option'''
    if option_type == "call":
        return norm.cdf(d1(price, strike, rf, years, volatility))
    elif option_type == "put":
        return norm.cdf(d1(price, strike, rf, years, volatility))-1

def rho(option_type, price, strike, rf, years, volatility):
    '''returns the rho of the option'''
    if option_type == "call":
        return (strike*years*np.exp(-rf*years)*norm.cdf(d2(price, strike, rf, years, volatility)))/100
    elif option_type == "put":
        return (-strike*years*np.exp(-rf*years)*norm.cdf(-d2(price, strike, rf, years, volatility)))/100