import pandas as pd
import yfinance as yf 

def fetch_data(ticker : str, period = "1y", interval = "1d") -> pd.DataFrame :
    df = yf.download(tickers=ticker,period=period, interval=interval)

    if df.empty:
        raise ValueError(f"no data found for {ticker}")
    
    if isinstance(df.columns[0], tuple):
        df.columns = [col[0] for col in df.columns]
    
    df.rename(columns={
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume"
    }, inplace=True)
    
    return df

