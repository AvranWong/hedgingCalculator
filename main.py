import pandas as pd 
import pandas_datareader as pdr
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt

#Function that fetches the pricing data for a period
def getData(longToken,shortToken):
    tickers = [longToken,shortToken]
    #Download closing prices
    start = dt.datetime(2020, 1, 1)
    end = dt.datetime(2022, 1, 1)
    data = pdr.get_data_yahoo(tickers, start, end)[["Close"]]
    data = data["Close"]
    return data

#Function that takes in the token symbol list and outputs a list of the latest prices
def getLatestPrice(data):
    prices = list(data.iloc[-1])
    return prices

#Passes in token list and calculates the assets delta against BTC
def getAssetDelta(tokens,data):
    #Empty list to hold the average delta values of tokens against BTC
    delta=[]
    #Calculates percentage change of BTC as benchmark
    data["BTCDailyChange"] = (data["BTC-USD"].div(data["BTC-USD"].shift(1))-1)
    for token in tokens:
        #Calculates the percentage change of each token
        data[token+"DailyChange"] =(data[token].div(data[token].shift(1))-1)
        data[token+"Sensitivity"] = data[token + "DailyChange"]/data["BTCDailyChange"]
        delta.append(data[token+"Sensitivity"].mean())
    return delta

def getWeight(tokens,data):
    weights = []
    #Gets latest prices of relevant tokens
    prices = getLatestPrice(data)
    return weights

#Function that takes in user inputs and outputs a delta number
def calcPortDelta(userInput):
    tokens = ["BTC-USD","ETH-USD"]
    #Fetches pricing data of relevant tokens, currently hardcorded
    data = getData("BTC-USD","ETH-USD")
    weights = getWeight(tokens,data)
    delta = getAssetDelta(tokens,data)
    
    portDelta = weights.dot(delta)
