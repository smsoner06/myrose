import asyncio
import random
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import traceback

# Telegram bot token ve chat ID'ler
TOKEN = '7495525753:AAEPhxeNxgL3nlop7UrBF-b37tJym4_UEtU'
CHAT_ID = ['-1002163566439']  # Birden fazla chat ID

# Mesajları tanımlayın
MESSAGES = [
    "*Deneme Bonuslarını görmek için butona tıklayabilirsiniz!*\nHemen fırsatları keşfedin.\n\n *Casino Bonus Platformu*",
    "*Yeni fırsatlar ve bonuslar için siteyi ziyaret edin!*\nBu fırsatlar kaçmaz.\n\n *Casino Bonus Platformu*",
    "*Bir sitenin linkini öğrenmek için*\nŞunu deneyin!\n\nÖrn: pusulabetlink\n\n *Casino Bonus Platformu*",
    "*En son bonus tekliflerimiz burada! Butona tıklayın.*\nGünün fırsatlarını kaçırmayın.\n\n *Casino Bonus Platformu*",
    "*Büyük ödüller sizi bekliyor! Hemen kontrol edin!*\nŞansınızı deneyin.\n\n *Casino Bonus Platformu*"
]

# Otomatik mesaj gönderim fonksiyonu
async def send_reminder():
    try:
        bot = Bot(token=TOKEN)
        button = InlineKeyboardButton("Deneme Bonusları", url="http://casinobonusplatformu.my.canva.site")
        markup = InlineKeyboardMarkup([[button]])

        for chat_id in CHAT_ID:
            message = random.choice(MESSAGES)  # Rastgele mesaj seçimi
            await bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown', reply_markup=markup)
        print("Message sent successfully to all chat IDs!")
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

# Scheduler başlatma
scheduler = AsyncIOScheduler()
scheduler.add_job(send_reminder, 'interval', minutes=10)  # Gönderim aralığını 5 dakikaya ayarla
scheduler.start()

# Event loop başlatma
loop = asyncio.get_event_loop()
loop.run_forever()
