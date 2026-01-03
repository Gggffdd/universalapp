import sqlite3
import json
from datetime import datetime

DATABASE_NAME = "universal_exchange.db"

def get_connection():
    """Получение соединения с БД"""
    return sqlite3.connect(DATABASE_NAME, check_same_thread=False)

async def init_database():
    """Инициализация базы данных"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Таблица пользователей
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        full_name TEXT,
        rub_balance REAL DEFAULT 0,
        ton_balance REAL DEFAULT 0,
        usdt_balance REAL DEFAULT 0,
        is_admin BOOLEAN DEFAULT FALSE,
        is_banned BOOLEAN DEFAULT FALSE,
        registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # ... остальные таблицы ...
    
    conn.commit()
    conn.close()
    print("✅ База данных инициализирована")
