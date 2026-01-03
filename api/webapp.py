import os
import json
from datetime import datetime
from aiohttp import web
import aiohttp_jinja2
import jinja2
import sqlite3
from pathlib import Path

from database.database import Database

# Настройка Jinja2
template_dir = Path(__file__).parent.parent / "web" / "templates"
env = aiohttp_jinja2.setup(
    web.Application(),
    loader=jinja2.FileSystemLoader(str(template_dir))
)

async def handle_index(request):
    """Главная страница Web App"""
    return aiohttp_jinja2.render_template(
        "index.html",
        request,
        {
            "title": "Universal Exchange",
            "timestamp": datetime.now().isoformat()
        }
    )

async def handle_profile(request):
    """Страница профиля"""
    user_id = request.query.get("user_id")
    if not user_id:
        return web.Response(text="User ID required", status=400)
    
    # Получаем данные пользователя
    user = Database.get_user(int(user_id))
    if not user:
        return web.Response(text="User not found", status=404)
    
    stats = Database.get_user_stats(int(user_id))
    
    return aiohttp_jinja2.render_template(
        "profile.html",
        request,
        {
            "user": user,
            "stats": stats,
            "timestamp": datetime.now().isoformat()
        }
    )

async def handle_exchange(request):
    """Страница обмена"""
    return aiohttp_jinja2.render_template(
        "exchange.html",
        request,
        {
            "title": "Обмен валюты",
            "timestamp": datetime.now().isoformat()
        }
    )

async def handle_products(request):
    """Страница товаров"""
    categories = Database.get_categories()
    products = Database.get_products(active_only=True)
    
    return aiohttp_jinja2.render_template(
        "products.html",
        request,
        {
            "categories": categories,
            "products": products,
            "title": "Товары",
            "timestamp": datetime.now().isoformat()
        }
    )

async def handle_api_data(request):
    """API для данных Web App"""
    action = request.query.get("action")
    
    if action == "rates":
        from bot.core import rate_manager
        rates = await rate_manager.get_cached_rates()
        
        return web.json_response({
            "success": True,
            "data": rates
        })
    
    elif action == "user":
        user_id = request.query.get("user_id")
        if user_id:
            user = Database.get_user(int(user_id))
            stats = Database.get_user_stats(int(user_id))
            
            return web.json_response({
                "success": True,
                "data": {
                    "user": user,
                    "stats": stats
                }
            })
    
    return web.json_response({
        "success": False,
        "error": "Invalid action"
    }, status=400)

# Создание приложения
app = web.Application()

# Настройка статических файлов
static_dir = Path(__file__).parent.parent / "web" / "static"
app.router.add_static("/static/", static_dir, name="static")

# Маршруты
app.router.add_get("/", handle_index)
app.router.add_get("/profile", handle_profile)
app.router.add_get("/exchange", handle_exchange)
app.router.add_get("/products", handle_products)
app.router.add_get("/api/data", handle_api_data)

# Для Vercel
async def handler(request):
    return await app.handle_request(request)

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=3000)
