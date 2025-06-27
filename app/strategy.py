from finta import TA
from app.fetch_data import fetch_data

# Apply strategy to current data (live mode)
def apply_strategy(ticker: str, period="1y",interval = "1d") -> dict:
    df = fetch_data(ticker,period,interval)

    # Add indicators
    df['rsi'] = TA.RSI(df)
    df['20dma'] = TA.SMA(df, period=20)
    df['50dma'] = TA.SMA(df, period=50)
    df.dropna(inplace=True)

    # Check last row for strategy condition
    last = df.iloc[-1]
    if last['rsi'] < 30 and last['20dma'] > last['50dma']:
        return {
            "signal": "BUY",
            "price": round(last['close'], 2),
            "ticker": ticker,
            "quantity": 2,
            "date": str(df.index[-1].date())
        }
    else:
        return {
            "signal": "NO_ACTION",
            "reason": "Conditions not met",
            "ticker": ticker,
            "date": str(df.index[-1].date())
        }

# Backtesting over historical data
def backtest_strategy(ticker: str, period="1y",interval = "1d") -> dict:
    df = fetch_data(ticker, period=period,interval=interval)

    # Add indicators
    df['rsi'] = TA.RSI(df)
    df['20dma'] = TA.SMA(df, period=20)
    df['50dma'] = TA.SMA(df, period=50)
    df.dropna(inplace=True)
    print(df)
    df.to_csv("data.csv")
    trades = []
    for i in range(len(df)):
        row = df.iloc[i]
        if row['rsi'] < 30 and row['20dma'] > row['50dma']:
            trades.append({
                "signal": "BUY",
                "price": round(row['close'], 2),
                "ticker": ticker,
                "quantity": 2,
                "date": str(df.index[i].date())
            })
    print(trades)
    return {"trades": trades}


