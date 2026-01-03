import os
import json
import asyncio
import sqlite3
from datetime import datetime
from http import HTTPStatus
from typing import Dict, Any

from aiogram import Bot, Dispatcher, types
from aiogram.types import Update
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

# Импорт ваших модулей
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.core import init_bot, dp, bot
from database.database import init_database, Database
from utils.helpers import format_number

# Получение переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")
WEBHOOK_PATH = "/bot"
WEBAPP_URL = os.getenv("WEBAPP_URL", "")

async def on_startup(app: web.Application):
    """Действия при запуске"""
    # Инициализация базы данных
    await init_database()
    
    # Установка вебхука
    webhook_url = f"{WEBAPP_URL}{WEBHOOK_PATH}"
    await bot.set_webhook(
        webhook_url,
        secret_token=WEBHOOK_SECRET,
        drop_pending_updates=True
    )
    
    print(f"🤖 Бот запущен. Webhook: {webhook_url}")

async def on_shutdown(app: web.Application):
    """Действия при остановке"""
    await bot.delete_webhook()
    await bot.session.close()
    print("🤖 Бот остановлен")

async def handle_webhook(request: web.Request):
    """Обработчик вебхуков от Telegram"""
    if WEBHOOK_SECRET:
        secret = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
        if secret != WEBHOOK_SECRET:
            return web.Response(status=403, text="Forbidden")
    
    try:
        update_data = await request.json()
        update = Update(**update_data)
        await dp.feed_update(bot, update)
        return web.Response(text="OK")
    except Exception as e:
        print(f"❌ Ошибка обработки вебхука: {e}")
        return web.Response(status=500, text="Internal Server Error")

async def handle_health(request: web.Request):
    """Health check endpoint"""
    return web.json_response({
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "service": "universal-exchange-bot"
    })

async def handle_stats(request: web.Request):
    """API для получения статистики"""
    try:
        # Получаем курсы
        from bot.core import rate_manager
        rates = await rate_manager.get_cached_rates()
        
        # Получаем статистику пользователей
        users_count = Database.get_user_count()
        active_users = Database.get_active_users_count()
        
        return web.json_response({
            "status": "success",
            "data": {
                "rates": {
                    "ton": rates.get('ton_sell_rate_rub', 0),
                    "usdt": rates.get('usdt_sell_rate_rub', 0),
                    "updated": rates.get('timestamp', '')
                },
                "users": {
                    "total": users_count,
                    "active": active_users,
                    "today": Database.get_users_today_count()
                },
                "timestamp": datetime.now().isoformat()
            }
        })
    except Exception as e:
        return web.json_response({
            "status": "error",
            "message": str(e)
        }, status=500)

# Создание aiohttp приложения
app = web.Application()

# Настройка маршрутов
app.router.add_post(WEBHOOK_PATH, handle_webhook)
app.router.add_get("/health", handle_health)
app.router.add_get("/api/stats", handle_stats)

# События жизненного цикла
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

# Для запуска на Vercel
async def handler(request):
    """Обработчик для Vercel"""
    return await app.handle_request(request)

# Для локального запуска
if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=8080)
