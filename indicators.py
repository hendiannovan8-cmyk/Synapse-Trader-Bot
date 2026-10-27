from ta.volatility import AverageTrueRange, BollingerBands

def calculate_supertrend(df, period=10, multiplier=3):
    hl2 = (df['High'] + df['Low']) / 2
    atr = AverageTrueRange(
        high=df['High'], low=df['Low'], close=df['Close'], window=period
    ).average_true_range()

    upper = (hl2 + multiplier * atr).values.copy()
    lower = (hl2 - multiplier * atr).values.copy()
    close = df['Close'].values
    st = [0.0] * len(df)
    trend = [True] * len(df)

    for i in range(1, len(df)):
        if close[i] > upper[i - 1]:
            trend[i] = True
        elif close[i] < lower[i - 1]:
            trend[i] = False
        else:
            trend[i] = trend[i - 1]
            if trend[i] and lower[i] < lower[i - 1]:
                lower[i] = lower[i - 1]
            if not trend[i] and upper[i] > upper[i - 1]:
                upper[i] = upper[i - 1]
        st[i] = lower[i] if trend[i] else upper[i]

    df['Supertrend'] = st
    df['Supertrend_Direction'] = trend
    return df

def add_indicators(df):
    bb = BollingerBands(close=df['Close'], window=20, window_dev=2)
    df['BB_Middle'] = bb.bollinger_mavg()
    df['BB_Upper'] = bb.bollinger_hband()
    df['BB_Lower'] = bb.bollinger_lband()
    df['ATR'] = AverageTrueRange(
        high=df['High'], low=df['Low'], close=df['Close'], window=14
    ).average_true_range()
    return df

def evaluate(df):
    row = df.iloc[-1]
    price = row['Close']
    if row['Supertrend_Direction'] and price <= row['BB_Lower']:
        return 'BUY', price, price - row['ATR'] * 1.5
    if (not row['Supertrend_Direction']) and price >= row['BB_Upper']:
        return 'SELL', price, price + row['ATR'] * 1.5
    return 'HOLD', price, 0