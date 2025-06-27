# app/services/sheet_logger.py

import pygsheets
import pandas as pd

# Authenticate with Google Sheets
gc = pygsheets.authorize(service_file='service_account.json')
print(gc)
SHEET_NAME = "Algo Trading Log"  


def log_closed_trade(trade: dict):
    try:
        sheet = gc.open(SHEET_NAME)
        print("Opened sheet:", sheet.title)

        try:
            wks = sheet.worksheet_by_title("Trade Log")
        except pygsheets.WorksheetNotFound:
            wks = sheet.add_worksheet("Trade Log", rows=1000, cols=20)

        df = pd.DataFrame([trade])

        #  Counting filled to append after that.
        filled_rows = len(wks.get_col(1, include_empty=False))
        next_row = filled_rows + 1

        # Resize if needed
        if next_row >= wks.rows:
            wks.resize(rows=wks.rows + 1000, cols=wks.cols)

    
        if filled_rows == 0:
            wks.set_dataframe(df, start='A1', copy_head=True)
        else:
            wks.set_dataframe(df, start=(next_row, 1), copy_head=False)

        print(f"Trade logged at row {next_row}")
        return "Trade logged successfully."

    except Exception as e:
        print(" Error:", str(e))
        return f"Error logging trade: {str(e)}"


# log_closed_trade(
#     {
#   "entry_date": "2025-06-25",
#   "exit_date": "2025-06-26",
#   "ticker": "TCS.NS",
#   "side": "BUY",
#   "entry_price": 3680.10,
#   "exit_price": 3750.25,
#   "quantity": 2,
#   "pnl": 70.15,
#   "status": "CLOSED",
#   "ml_signal": "UP",
#   "strategy_match": True
# }

# )
