import telebot
import ccxt
import pandas as pd
import config
from sqlalchemy import create_engine
from indicators import calculate_supertrend, add_indicators, evaluate  # <-- Diimpor langsung

telegram_token = config.telegram_token
bot = telebot.TeleBot(telegram_token)
exchange = ccxt.indodax()
engine = create_engine(config.DATABASE_URL, pool_pre_ping = True)

# ... (kode handler /sinyal Anda menjadi sangat bersih):
@bot.message_handler(commands=['sinyal'])
def cek_sinyal(message):
    try:
        bot.reply_to(message, "🔍 Mengambil data dari Cloud Database & menghitung indikator...")
        
        df_market = pd.read_sql('data_btc', con=engine).dropna()
        
        # Menggunakan fungsi dari file indicators.py
        df_market = calculate_supertrend(df_market)
        df_market = add_indicators(df_market)
        decision, entry_price, stop_loss = evaluate(df_market)

        output = (
            f"🤖 *Analisis Sinyal Bot (Supertrend + BB)*\n\n"
            f"📌 *Keputusan:* `{decision}`\n"
            f"💰 *Harga Saat Ini:* Rp {entry_price:,.0f}\n"
        )
        if decision in ['BUY', 'SELL']:
            output += f"🛑 *Rekomendasi Stop Loss:* Rp {stop_loss:,.0f}\n"
        else:
            output += f"ℹ️ *Status:* Pasar dalam kondisi Hold / Sideways."

        bot.reply_to(message, output, parse_mode='Markdown')

    except Exception as e:
        bot.reply_to(message, 'Gagal memproses analisis sinyal dari database.')
        print(f'Detail Error: {e}')
if __name__ == "__main__":
    print("Bot Telegram notifier berjalan...", flush=True)
    bot.infinity_polling()
# ... (lanjutan handler lainnya)