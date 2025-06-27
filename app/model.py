import numpy as np
from finta import TA
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

FEATURES = ['rsi', 'macd', 'volume']

def add_ml_features(df):
    df['rsi'] = TA.RSI(df)
    df['macd'] = TA.MACD(df)['MACD']
    df['volume'] = df['volume']

    
    df['target'] = np.where(df['close'].shift(-1) > df['close'], 1, 0)

  
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(inplace=True)
    return df

def train_model(df):
    X = df[FEATURES]
    y = df['target']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    return model, accuracy

def predict_next_movement(model, df):
    latest = df[FEATURES].iloc[[-1]]
    pred = model.predict(latest)[0]
    return "UP" if pred == 1 else "DOWN"
