import os
from dotenv import load_dotenv

# Memuat file environment (ubah 'key.env' jika kamu tetap ingin pakai nama itu)
load_dotenv('.env') 

# Menyiapkan variabel yang dipanggil di file utama
indodax_api_key = os.getenv("INDODAX_API_KEY")
secret_api_key = os.getenv("INDODAX_SECRET_KEY")
DATABASE_URL = os.environ.get("DATABASE_URL")
telegram_token= os.environ.get("TELEGRAM_TOKEN")