from aiohttp import web
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
import os
from pathlib import Path

class WebApp:
    def __init__(self, bot: Bot, dp: Dispatcher):
        self.bot = bot
        self.dp = dp
        self.app = web.Application()
        
    async def handle_main_page(self, request):
        """Главная страница Web App"""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Universal Exchange Mini App</title>
            <script src="https://telegram.org/js/telegram-web-app.js"></script>
            <style>
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }
                
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    min-height: 100vh;
                    padding: 20px;
                }
                
                .container {
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                }
                
                header {
                    text-align: center;
                    margin-bottom: 40px;
                    padding-top: 40px;
                }
                
                h1 {
                    font-size: 2.5rem;
                    margin-bottom: 10px;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                }
                
                .subtitle {
                    font-size: 1.2rem;
                    opacity: 0.9;
                }
                
                .dashboard {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 20px;
                    margin-bottom: 40px;
                }
                
                .card {
                    background: rgba(255, 255, 255, 0.1);
                    backdrop-filter: blur(10px);
                    border-radius: 20px;
                    padding: 30px;
                    transition: transform 0.3s, background 0.3s;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                }
                
                .card:hover {
                    transform: translateY(-5px);
                    background: rgba(255, 255, 255, 0.2);
                }
                
                .card h3 {
                    font-size: 1.5rem;
                    margin-bottom: 15px;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }
                
                .card p {
                    font-size: 1rem;
                    line-height: 1.6;
                    opacity: 0.9;
                    margin-bottom: 20px;
                }
                
                .btn {
                    display: inline-block;
                    background: linear-gradient(45deg, #FF6B6B, #EE5A24);
                    color: white;
                    padding: 12px 30px;
                    border-radius: 50px;
                    text-decoration: none;
                    font-weight: bold;
                    text-align: center;
                    transition: transform 0.3s, box-shadow 0.3s;
                    border: none;
                    cursor: pointer;
                    width: 100%;
                    font-size: 1rem;
                }
                
                .btn:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 10px 20px rgba(255, 107, 107, 0.3);
                }
                
                .btn-secondary {
                    background: rgba(255, 255, 255, 0.2);
                    color: white;
                }
                
                .btn-secondary:hover {
                    background: rgba(255, 255, 255, 0.3);
                }
                
                .stats {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 15px;
                    margin-bottom: 30px;
                }
                
                .stat-item {
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 15px;
                    padding: 20px;
                    text-align: center;
                }
                
                .stat-value {
                    font-size: 2rem;
                    font-weight: bold;
                    margin-bottom: 5px;
                }
                
                .stat-label {
                    font-size: 0.9rem;
                    opacity: 0.8;
                }
                
                .section {
                    margin-bottom: 40px;
                }
                
                .section h2 {
                    font-size: 1.8rem;
                    margin-bottom: 20px;
                    border-bottom: 2px solid rgba(255, 255, 255, 0.2);
                    padding-bottom: 10px;
                }
                
                .features {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 20px;
                }
                
                .feature-item {
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 15px;
                    padding: 20px;
                }
                
                .feature-icon {
                    font-size: 2rem;
                    margin-bottom: 10px;
                }
                
                footer {
                    text-align: center;
                    margin-top: 50px;
                    padding: 20px;
                    border-top: 1px solid rgba(255, 255, 255, 0.2);
                    font-size: 0.9rem;
                    opacity: 0.8;
                }
                
                @media (max-width: 768px) {
                    .container {
                        padding: 10px;
                    }
                    
                    h1 {
                        font-size: 2rem;
                    }
                    
                    .dashboard {
                        grid-template-columns: 1fr;
                    }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <header>
                    <h1>💰 Universal Exchange</h1>
                    <p class="subtitle">Безопасный обмен криптовалют в Telegram</p>
                </header>
                
                <div class="section">
                    <div class="stats" id="stats">
                        <!-- Статистика будет загружена динамически -->
                        <div class="stat-item">
                            <div class="stat-value" id="ton-price">--</div>
                            <div class="stat-label">TON</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value" id="usdt-price">--</div>
                            <div class="stat-label">USDT</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value" id="users-count">--</div>
                            <div class="stat-label">Пользователей</div>
                        </div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>💱 Быстрый обмен</h2>
                    <div class="dashboard">
                        <div class="card">
                            <h3>💎 Купить TON</h3>
                            <p>Купить TON за рубли через Crypto Bot. Быстро и безопасно.</p>
                            <button class="btn" onclick="buyTON()">Купить TON</button>
                        </div>
                        
                        <div class="card">
                            <h3>💰 Купить USDT</h3>
                            <p>Купить USDT по лучшему курсу с мгновенным зачислением.</p>
                            <button class="btn" onclick="buyUSDT()">Купить USDT</button>
                        </div>
                        
                        <div class="card">
                            <h3>🔄 Продать крипту</h3>
                            <p>Продать TON или USDT за рубли на свою карту.</p>
                            <button class="btn btn-secondary" onclick="sellCrypto()">Продать</button>
                        </div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>🛒 Другие возможности</h2>
                    <div class="features">
                        <div class="feature-item">
                            <div class="feature-icon">👤</div>
                            <h4>Профиль</h4>
                            <p>Просмотр балансов, история операций, рефералы</p>
                            <button class="btn btn-secondary" onclick="openProfile()">Открыть</button>
                        </div>
                        
                        <div class="feature-item">
                            <div class="feature-icon">📦</div>
                            <h4>Товары</h4>
                            <p>Покупка цифровых товаров, игр, сервисов</p>
                            <button class="btn btn-secondary" onclick="openProducts()">Смотреть</button>
                        </div>
                        
                        <div class="feature-item">
                            <div class="feature-icon">👥</div>
                            <h4>Рефералы</h4>
                            <p>Приглашайте друзей и получайте бонусы</p>
                            <button class="btn btn-secondary" onclick="openReferrals()">Подробнее</button>
                        </div>
                        
                        <div class="feature-item">
                            <div class="feature-icon">📞</div>
                            <h4>Поддержка</h4>
                            <p>Помощь по операциям, ответы на вопросы</p>
                            <button class="btn btn-secondary" onclick="openSupport()">Связаться</button>
                        </div>
                    </div>
                </div>
                
                <footer>
                    <p>© 2024 Universal Exchange. Все права защищены.</p>
                    <p>Время работы: круглосуточно</p>
                </footer>
            </div>
            
            <script>
                // Инициализация Telegram Web App
                const tg = window.Telegram.WebApp;
                tg.expand();
                tg.MainButton.show();
                
                // Загрузка данных
                async function loadData() {
                    try {
                        const response = await fetch('/api/stats');
                        const data = await response.json();
                        
                        document.getElementById('ton-price').textContent = data.ton_price + ' ₽';
                        document.getElementById('usdt-price').textContent = data.usdt_price + ' ₽';
                        document.getElementById('users-count').textContent = data.users_count;
                    } catch (error) {
                        console.error('Ошибка загрузки данных:', error);
                    }
                }
                
                // Функции для кнопок
                function buyTON() {
                    tg.showPopup({
                        title: 'Покупка TON',
                        message: 'Выберите способ оплаты:',
                        buttons: [
                            {id: 'ton_rub', text: '💳 Рубли', type: 'default'},
                            {id: 'ton_usdt', text: '💰 USDT (Crypto Bot)', type: 'default'},
                            {id: 'cancel', text: 'Отмена', type: 'cancel'}
                        ]
                    }, function(buttonId) {
                        if (buttonId === 'ton_rub') {
                            startTONPurchase('rub');
                        } else if (buttonId === 'ton_usdt') {
                            startTONPurchase('usdt');
                        }
                    });
                }
                
                function buyUSDT() {
                    tg.showPopup({
                        title: 'Покупка USDT',
                        message: 'Введите сумму для покупки:',
                        buttons: [
                            {id: 'confirm', text: 'Продолжить', type: 'default'},
                            {id: 'cancel', text: 'Отмена', type: 'cancel'}
                        ]
                    });
                }
                
                function sellCrypto() {
                    tg.showPopup({
                        title: 'Продажа криптовалюты',
                        message: 'Выберите валюту для продажи:',
                        buttons: [
                            {id: 'sell_ton', text: '💎 TON', type: 'default'},
                            {id: 'sell_usdt', text: '💰 USDT', type: 'default'},
                            {id: 'cancel', text: 'Отмена', type: 'cancel'}
                        ]
                    });
                }
                
                function openProfile() {
                    tg.MainButton.setText('Профиль');
                    tg.MainButton.show();
                    tg.MainButton.onClick(() => {
                        tg.sendData(JSON.stringify({action: 'open_profile'}));
                    });
                }
                
                function openProducts() {
                    tg.MainButton.setText('Товары');
                    tg.MainButton.show();
                    tg.MainButton.onClick(() => {
                        tg.sendData(JSON.stringify({action: 'open_products'}));
                    });
                }
                
                function openReferrals() {
                    tg.MainButton.setText('Рефералы');
                    tg.MainButton.show();
                    tg.MainButton.onClick(() => {
                        tg.sendData(JSON.stringify({action: 'open_referrals'}));
                    });
                }
                
                function openSupport() {
                    tg.openTelegramLink('https://t.me/salxanovka');
                }
                
                async function startTONPurchase(currency) {
                    const result = await tg.showPopup({
                        title: 'Введите сумму',
                        message: `Введите сумму в ${currency === 'rub' ? 'рублях' : 'USDT'}:`,
                        buttons: [
                            {id: 'confirm', text: 'Продолжить', type: 'default'},
                            {id: 'cancel', text: 'Отмена', type: 'cancel'}
                        ]
                    });
                    
                    if (result === 'confirm') {
                        tg.sendData(JSON.stringify({
                            action: 'buy_ton',
                            currency: currency,
                            amount: 1000 // Здесь будет фактическая сумма
                        }));
                    }
                }
                
                // Обработка данных от бота
                tg.onEvent('webAppDataReceived', (event) => {
                    const data = JSON.parse(event.data);
                    console.log('Получены данные:', data);
                    
                    if (data.action === 'close') {
                        tg.close();
                    }
                });
                
                // Загрузка данных при старте
                loadData();
                
                // Обновление данных каждые 30 секунд
                setInterval(loadData, 30000);
            </script>
        </body>
        </html>
        """
        return web.Response(text=html_content, content_type='text/html')
    
    async def handle_api_stats(self, request):
        """API для получения статистики"""
        # Получаем курсы и статистику из вашей БД
        rates = await rate_manager.get_cached_rates()
        
        # Получаем количество пользователей
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        users_count = cursor.fetchone()[0]
        conn.close()
        
        stats = {
            'ton_price': rates.get('ton_sell_rate_rub', 0),
            'usdt_price': rates.get('usdt_sell_rate_rub', 0),
            'users_count': users_count,
            'timestamp': datetime.now().isoformat()
        }
        
        return web.json_response(stats)
    
    def setup_routes(self):
        """Настройка маршрутов"""
        self.app.router.add_get('/', self.handle_main_page)
        self.app.router.add_get('/api/stats', self.handle_api_stats)
        
        # Добавляем обработчик вебхуков от Telegram
        SimpleRequestHandler(
            dispatcher=self.dp,
            bot=self.bot,
            secret_token=os.getenv('WEBHOOK_SECRET', 'your_secret_token')
        ).register(self.app, path='/webhook')
    
    async def start(self, host='0.0.0.0', port=8080):
        """Запуск Web App"""
        self.setup_routes()
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, host, port)
        await site.start()
        
        print(f"🌐 Web App запущен на http://{host}:{port}")
        
        # Бесконечный цикл
        await asyncio.Future()
