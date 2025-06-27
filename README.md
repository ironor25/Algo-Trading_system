# Algo Trading System with Strategy + ML + Sheet Automation

This is an end-to-end algo trading system that combines:

* Technical strategy (RSI + DMA)
* Machine learning (Logistic Regression)
* Trade execution tracking
* Google Sheets logging
* REST API (via FastAPI)

---

## 🚀 Features

* ✅ Apply trading strategy (RSI < 30 & 20DMA > 50DMA)
* ✅ Confirm with ML prediction (Logistic Regression)
* ✅ Automatically execute trades
* ✅ Log open/close trades
* ✅ Google Sheets logging with PnL
* ✅ REST API endpoints for all operations

---

## 📦 Folder Structure

```
app/
├── api/
│   └── routes.py              # All API endpoints
├── models/
│   └── model.py              # ML model functions
├── services/
│   ├── data_fetcher.py       # yfinance fetcher
│   ├── strategy.py           # Trading strategy logic
│   ├── trade_manager.py      # Manage trade state
│   └── sheet_logger.py       # Google Sheets logger
├── main.py                   # FastAPI app
├── requirements.txt
└── service_account.json      # Google Sheets service account key
```

---

## 🛠 Setup Instructions

### 1. Clone and install dependencies

```bash
git clone <repo-url>
cd <project-folder>
pip install -r requirements.txt
```

### 2. Enable Google APIs

* Go to [Google Cloud Console](https://console.cloud.google.com/)
* Enable **Google Sheets API** and **Google Drive API**
* Download the `service_account.json` and place it in the root folder
* Share your Google Sheet with the service account email

### 3. Create a Google Sheet

* Title: `Algo Trading Log`
* Add a tab: `Trade Log`

---

## ⚙️ Running the Server

```bash
uvicorn app.main:app --reload
```

---

## 🔗 API Endpoints

### 1. Apply Strategy

```
GET /strategy/apply/{ticker}
```

Returns signal if conditions are met.

### 2. Backtest Strategy

```
GET /strategy/backtest/{ticker}
```

Returns list of past BUY signals.

### 3. ML Prediction

```
POST /ml-predict
```

Returns UP/DOWN based on ML model.

### 4. Auto Trade (Execute or Close)

```
POST /auto-trade
```

* Body (to open): `{ "ticker": "TCS.NS" }`
* Body (to close): `{ "ticker": "TCS.NS", "exit_price": 3740.5 }`





## 📒 Google Sheets Log Example

Each row will contain:

```
entry_date, exit_date, ticker, side, entry_price, exit_price,
quantity, pnl, status, ml_signal, strategy_match
```

---
