import time
import ccxt
import pandas as pd
import config
from sqlalchemy import create_engine  # <-- Tambahan untuk database

engine = create_engine(config.DATABASE_URL)

exchange = ccxt.indodax({
    'apiKey': config.indodax_api_key,
    'secret': config.secret_api_key,
})

print('Starting Real-Time Market Data Producer with Cloud DB...\n')

while True:
  try:
    bars = exchange.fetch_ohlcv('BTC/IDR', timeframe='15m', limit=200)

    df_market = pd.DataFrame(
        bars, columns=['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
    )
    df_market['Timestamp'] = pd.to_datetime(df_market['Timestamp'], unit='ms')

    # --- PERUBAHAN UTAMA ---
    # Alih-alih .to_csv(), data langsung dikirim ke tabel database online bernama 'data_btc'
    df_market.to_sql('data_btc', engine, if_exists='replace', index=False)

    current_time = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{current_time}] Successfully updated Cloud Database!')
    print('-' * 60)

  except Exception as error:
    print(f'[ERROR] Failed to fetch market data: {error}')

  print('Waiting for the next polling cycle...\n')
  time.sleep(900)