from app.strategy import apply_strategy
from app.model import add_ml_features, train_model, predict_next_movement
import pandas as pd
from app.log_trade import log_closed_trade
from app.fetch_data import fetch_data
# In-memory store for open trades
open_trades = {}




def execute_trade(ticker: str,exit_price : float = None):
    df = fetch_data(ticker)
    df = add_ml_features(df)
    model, accuracy = train_model(df)
    prediction = predict_next_movement(model, df)
    if exit_price == None:
    # Step 1: Fetch and check strategy
        result = apply_strategy(ticker)
        if result["signal"] != "BUY":
            return {"message": "No trade signal", "details": result}

        # Step 2: Predict next price using ML
        

        if prediction != "UP":
            return {"message": "ML doesn't confirm", "prediction": prediction}

        # Step 3: Place order (store in memory)
        trade = {
            "entry_date": result['date'],
            "ticker": result['ticker'],
            "side": result['signal'],
            "entry_price": result['price'],
            "quantity": result['quantity'],
          
        }
        open_trades[ticker] = trade

        return {
            "message": "Trade executed",
            "trade": trade
        }
    
    else:
        if ticker not in open_trades:
            return {"message": "No open trade for this ticker"}

        trade = open_trades.pop(ticker)
        trade["exit_price"] = exit_price
        trade["exit_date"] = str(pd.Timestamp.today().date())
        trade["pnl"] = round(exit_price - trade["entry_price"], 2)
        trade["status"] = "CLOSED"
        trade["ml_signal"] = prediction
        trade["strategy"] = True



        log_closed_trade(trade)
        return {
            "message": "Trade closed and logged",
            "trade": trade
        }
