# app/api/routes.py

from fastapi import FastAPI
from pydantic import BaseModel
from app.services.strategy import apply_strategy, backtest_strategy
from app.services.fetch_data import fetch_data
from app.services.model import add_ml_features, train_model, predict_next_movement
from app.services.auto_trigger import execute_trade
from app.services.log_trade import log_closed_trade

router = FastAPI()

# In-memory trade store for demo
open_trades = {}

class TickerRequest(BaseModel):
    ticker: str | None = None
    exit_price: float | None = None
    period: str | None = "1y"
    interval: str | None = "1D"
    trades: dict | None = None

@router.get("/strategy/apply")
def apply_strategy_route(req: TickerRequest):
    result = apply_strategy(req.ticker,req.period,req.interval)
    return result

@router.get("/strategy/backtest")
def backtest_strategy_route(req: TickerRequest):
    result = backtest_strategy(req.ticker,req.period,req.interval)
    return result

@router.post("/ml-predict")
def predict_ml_route(req: TickerRequest):
    df = fetch_data(req.ticker,req.period,req.interval)
    df = add_ml_features(df)
    model, acc = train_model(df)
    prediction = predict_next_movement(model, df)
    return {
        "accuracy": acc,
        "prediction": prediction
    }

@router.post("/auto-trade")
def auto_trade(req: TickerRequest):
    if req.exit_price is not None:
        return execute_trade(req.ticker, req.exit_price)
    else:
        return execute_trade(req.ticker)

