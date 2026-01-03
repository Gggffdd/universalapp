import os
import asyncio
import logging
from typing import Dict, Any

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo,
    ReplyKeyboardMarkup,
    KeyboardButton
)

from database.database import Database, init_database
from utils.helpers import format_number
from utils.rates import RealRateManager

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()

# Менеджер курсов
rate_manager = RealRateManager()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    """Команда /start с Web App кнопкой"""
    user_id = message.from_user.id
    username = message.from_user.username or ""
    full_name = message.from_user.full_name
    
    # Создаем или обновляем пользователя
    user = Database.get_user(user_id)
    if not user:
        Database.create_user(user_id, username, full_name)
    
    # Получаем URL Web App
    webapp_url = os.getenv("WEBAPP_URL", "https://your-project.vercel.app")
    
    # Создаем клавиатуру с Web App кнопкой
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🌐 Открыть Web App", web_app=WebAppInfo(url=webapp_url))],
            [KeyboardButton(text="💱 Обмен валют")],
            [KeyboardButton(text="🛒 Товары")],
            [KeyboardButton(text="👤 Профиль")],
            [KeyboardButton(text="📞 Поддержка")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие"
    )
    
    await message.answer(
        f"""<b>🤖 Добро пожаловать в Universal Exchange, {full_name}!</b>

💱 <b>Мы предоставляем:</b>
• Мгновенный обмен TON/USDT
• Безопасные криптоплатежи через Crypto Bot
• Широкий выбор товаров
• Реферальную программу

📱 <b>Для удобной работы рекомендуем:</b>
1. Нажмите кнопку "🌐 Открыть Web App"
2. Используйте удобный интерфейс в браузере
3. Совершайте операции в один клик!

👇 <b>Выберите действие:</b>""",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

@dp.message(lambda message: message.text == "🌐 Открыть Web App")
async def open_webapp(message: types.Message):
    """Открытие Web App"""
    webapp_url = os.getenv("WEBAPP_URL", "https://your-project.vercel.app")
    
    await message.answer(
        "🌐 Открываю Web App...",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📱 Открыть в браузере",
                        web_app=WebAppInfo(url=webapp_url)
                    )
                ]
            ]
        )
    )

@dp.message(Command("webapp"))
async def cmd_webapp(message: types.Message):
    """Команда /webapp"""
    webapp_url = os.getenv("WEBAPP_URL", "https://your-project.vercel.app")
    
    await message.answer(
        """<b>🌐 Universal Exchange Web App</b>

📱 <b>Преимущества Web App:</b>
• Удобный интерфейс на весь экран
• Мгновенные уведомления
• Быстрые операции в один клик
• Поддержка темной темы
• Работает в любом браузере

👇 <b>Нажмите кнопку ниже чтобы открыть:</b>""",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🚀 Открыть Web App",
                        web_app=WebAppInfo(url=webapp_url)
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="📊 Текущие курсы",
                        callback_data="current_rates"
                    )
                ]
            ]
        ),
        parse_mode="HTML"
    )

# Добавьте сюда остальные обработчики из вашего кода
