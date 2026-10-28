import os
from dotenv import load_dotenv

# Memuat file environment
load_dotenv('.env')

# Menyiapkan variabel yang dipanggil di file utama
indodax_api_key = os.getenv("indodax_api_key")
secret_api_key = os.getenv("secret_api_key")
DATABASE_URL = os.getenv("DATABASE_URL")
telegram_token = os.getenv("telegram_token")