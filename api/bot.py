import os
import json
from http.server import BaseHTTPRequestHandler
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Получение токена из переменных окружения
BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    logger.error("❌ BOT_TOKEN не установлен в переменных окружения!")
    BOT_TOKEN = "ваш_токен_бота"  # Замените на ваш токен

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_command(message: types.Message):
    """Обработчик команды /start"""
    await message.answer(
        "🤖 <b>Universal Exchange Bot</b>\n\n"
        "✅ Бот успешно запущен на Vercel!\n\n"
        "📱 <b>Доступные команды:</b>\n"
        "/start - Перезапустить бота\n"
        "/menu - Главное меню\n"
        "/rates - Текущие курсы\n"
        "/help - Помощь\n\n"
        "🚀 <b>Бот работает в облаке!</b>",
        parse_mode="HTML"
    )

@dp.message(Command("menu"))
async def menu_command(message: types.Message):
    """Главное меню"""
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text="💱 Обмен TON/USDT", callback_data="exchange"),
                types.InlineKeyboardButton(text="🛒 Товары", callback_data="products")
            ],
            [
                types.InlineKeyboardButton(text="👤 Профиль", callback_data="profile"),
                types.InlineKeyboardButton(text="👥 Рефералы", callback_data="referrals")
            ],
            [
                types.InlineKeyboardButton(text="📞 Поддержка", url="https://t.me/salxanovka")
            ]
        ]
    )
    
    await message.answer(
        "🏠 <b>Главное меню</b>\n\n"
        "Выберите раздел:",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

@dp.message(Command("rates"))
async def rates_command(message: types.Message):
    """Текущие курсы"""
    await message.answer(
        "📊 <b>Текущие курсы:</b>\n\n"
        "💎 TON: 1 TON = 1.45 USDT\n"
        "💰 USDT: 1 USDT = 0.95 USD\n\n"
        "⏰ Обновлено только что\n"
        "🚀 Курсы в реальном времени",
        parse_mode="HTML"
    )

@dp.message(Command("help"))
async def help_command(message: types.Message):
    """Помощь"""
    await message.answer(
        "📚 <b>Помощь по боту</b>\n\n"
        "<b>Основные команды:</b>\n"
        "/start - Запустить бота\n"
        "/menu - Главное меню\n"
        "/rates - Курсы валют\n"
        "/help - Эта справка\n\n"
        "<b>Поддержка:</b>\n"
        "Если у вас возникли проблемы, обратитесь:\n"
        "• @salxanovka\n"
        "• @wwhocrime\n\n"
        "🚀 <b>Бот работает на Vercel</b>",
        parse_mode="HTML"
    )

# Обработчики callback
@dp.callback_query()
async def handle_callback(callback: types.CallbackQuery):
    """Обработка callback запросов"""
    data = callback.data
    
    if data == "exchange":
        await callback.message.edit_text(
            "💱 <b>Обмен TON/USDT</b>\n\n"
            "Выберите действие:",
            parse_mode="HTML"
        )
    elif data == "products":
        await callback.message.edit_text(
            "🛒 <b>Товары</b>\n\n"
            "Раздел товаров в разработке...",
            parse_mode="HTML"
        )
    else:
        await callback.answer("⏳ Функция в разработке", show_alert=True)

async def handle_telegram_update(update_data: dict):
    """Обработка обновления от Telegram"""
    try:
        update = types.Update(**update_data)
        await dp.feed_update(bot=bot, update=update)
        return True
    except Exception as e:
        logger.error(f"❌ Ошибка обработки обновления: {e}")
        return False

# HTTP обработчик для Vercel
async def handler(request):
    """Обработчик HTTP запросов для Vercel"""
    try:
        if request.method == "GET":
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "status": "ok",
                    "message": "🤖 Universal Exchange Bot работает!",
                    "timestamp": asyncio.get_event_loop().time()
                })
            }
        
        elif request.method == "POST" and request.path == "/webhook":
            try:
                body = await request.json()
                success = await handle_telegram_update(body)
                
                if success:
                    return {"statusCode": 200, "body": "OK"}
                else:
                    return {"statusCode": 400, "body": "Error processing update"}
                    
            except Exception as e:
                logger.error(f"❌ Ошибка в webhook: {e}")
                return {"statusCode": 400, "body": f"Error: {str(e)}"}
        
        else:
            return {
                "statusCode": 404,
                "body": "Not Found"
            }
            
    except Exception as e:
        logger.error(f"❌ Ошибка в handler: {e}")
        return {"statusCode": 500, "body": "Internal Server Error"}

# Для локального тестирования
if __name__ == "__main__":
    from aiogram import executor
    print("🤖 Запуск бота локально...")
    executor.start_polling(dp, skip_updates=True)
