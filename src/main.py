import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Конфигурация
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# Инициализация бота
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

async def main():
    """Основная функция запуска бота"""
    print("🤖 Бот запускается...")
    
    # Инициализация базы данных
    from database import init_database
    await init_database()
    
    # Регистрация обработчиков
    from handlers import user_handlers, admin_handlers, product_handlers
    
    # Запуск периодических задач
    from utils.rates import rate_manager
    asyncio.create_task(rate_manager.start_auto_update())
    
    # Настройка webhook для Vercel
    if os.getenv("VERCEL"):
        webhook_url = f"https://{os.getenv('VERCEL_URL')}/webhook"
        await bot.set_webhook(webhook_url)
        print(f"🌐 Webhook установлен: {webhook_url}")
    
    # Запуск бота
    if os.getenv("VERCEL"):
        # Для Vercel используется webhook
        from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
        from aiohttp import web
        
        app = web.Application()
        SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="/webhook")
        setup_application(app, dp, bot=bot)
        
        port = int(os.getenv("PORT", 3000))
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", port)
        await site.start()
        print(f"🚀 Сервер запущен на порту {port}")
        
        # Бесконечный цикл
        await asyncio.Event().wait()
    else:
        # Для локальной разработки
        await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
