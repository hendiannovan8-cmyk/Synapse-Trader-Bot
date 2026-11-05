import time
import pandas as pd
import telebot
import config
from sqlalchemy import create_engine
from indicators import calculate_supertrend, add_indicators, evaluate

# Hubungkan ke database dengan pool_pre_ping agar koneksi stabil
engine = create_engine(
    config.DATABASE_URL, 
    pool_pre_ping=True,
    connect_args={'prepare_threshold': None}
)

# Inisialisasi bot Telegram untuk pengiriman pesan otomatis
bot = telebot.TeleBot(config.telegram_token) if config.telegram_token else None
CHECK_INTERVAL = 60
last_alert = None  # Mencegah pengiriman notifikasi berulang pada candle yang sama

def notify(text):
    """Fungsi mandiri untuk mengirim push notification ke Telegram"""
    print(text, flush=True)
    if bot and getattr(config, 'TELEGRAM_CHAT_ID', None):
        try:
            bot.send_message(config.TELEGRAM_CHAT_ID, text, parse_mode='Markdown')
        except Exception as e:
            print(f"[ERROR] Gagal kirim Telegram: {e}", flush=True)

print("Strategy runner dimulai...", flush=True)

while True:
    try:
        # Ambil data dari tabel Supabase
        df = pd.read_sql('data_btc', con=engine).dropna().reset_index(drop=True)
        
        if len(df) < 30:
            print("Data belum cukup (minimal 30 baris), menunggu...", flush=True)
        else:
            # Hitung indikator menggunakan modul bersama (indicators.py)
            df = calculate_supertrend(df)
            df = add_indicators(df)
            
            # Evaluasi keputusan pasar
            decision, price, sl = evaluate(df)
            
            # Ambil timestamp candle terakhir
            candle_time = str(df.iloc[-1]['Timestamp']) if 'Timestamp' in df.columns else "latest"
            print(f"[{candle_time}] Evaluasi: {decision} @ Rp {price:,.0f}", flush=True)

            # Kirim notifikasi otomatis jika ada sinyal BUY / SELL dan belum pernah dikirim di candle ini
            if decision in ('BUY', 'SELL') and last_alert != (candle_time, decision):
                notify(
                    f"🚨 *Sinyal {decision} BTC/IDR*\n"
                    f"💰 Harga: Rp {price:,.0f}\n"
                    f"🛑 Stop Loss: Rp {sl:,.0f}"
                )
                last_alert = (candle_time, decision)
                
    except Exception as e:
        print(f"[ERROR] Strategi: {e}", flush=True)
        
    time.sleep(CHECK_INTERVAL)