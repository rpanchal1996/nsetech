import json
import pandas as pd
import json
import requests

def df_from_ticker(ticker):
    df = pd.DataFrame.from_dict(requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol='+ticker+'&outputsize=compact&apikey=OC7TVLG32OYGOGBQ').json()['Time Series (Daily)'], orient='index')
    df.columns = ['Open', 'High', 'Low', 'Close', 'AdjustedClose','Volume', 'Divident', 'SplitCoefficient']
    return df


def get_adj_close(df, n):
    return df[-n:]['AdjustedClose'].astype('float')

def get_volatility(ticker, n_days):
    df_ticker = get_adj_close(df_from_ticker(ticker))
    df_dji = get_adj_close(df_from_ticker("DJI"))
    std_tick = df_ticker.std()/df_ticker.mean()
    std_dji = df_dji.std()/df_dji.mean()
    return (std_tick - std_dji)/std_dji * 100

