import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os


# Bot token'ınızı buraya ekleyin
TOKEN = '7512751711:AAHirkd9efwwYkZKM7tnfp7g3Rqr_WMeEOM'

# Filtrelerin saklanacağı dosya
FILTERS_FILE = 'filters.json'


# Filtreleri dosyadan yükleyin
def load_filters():
    if os.path.exists(FILTERS_FILE):
        try:
            with open(FILTERS_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            # Dosya bozulmuşsa, boş bir sözlükle başlatın
            return {}
    else:
        # Dosya yoksa, boş bir sözlükle başlatın
        return {}


# Filtreleri dosyaya kaydedin
def save_filters(filters):
    with open(FILTERS_FILE, 'w') as f:
        json.dump(filters, f, indent=4)


# Filtreleri yükleyin
filters_data = load_filters()


# Yöneticileri kontrol eden yardımcı fonksiyon
async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    member = await context.bot.get_chat_member(chat_id, user_id)
    return member.status in ['administrator', 'creator']


# /addfilter komutu - yeni filtre ekler
async def add_filter(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await is_admin(update, context):
        await update.message.reply_text('Bu komutu sadece yöneticiler kullanabilir.')
        return

    if len(context.args) < 2:
        await update.message.reply_text('Lütfen şu formatta girin: /addfilter <kelime> <cevap>-<buton_linki>')
        return

    keyword = context.args[0].lower()
    # Cevap ve linki | karakteriyle ayırıyoruz
    try:
        response, button_link = ' '.join(context.args[1:]).split(' -', 1)
    except ValueError:
        await update.message.reply_text('Lütfen şu formatta girin: <cevap>-<buton_linki>')
        return

    filters_data[keyword] = {
        'response': response.strip(),
        'buttons': [{'text': 'Siteye Git', 'url': button_link.strip()}]
    }

    save_filters(filters_data)
    await update.message.reply_text(f'Filtre eklendi: {keyword} -> {response.strip()} (Link: {button_link.strip()})')


# /deletefilter komutu - filtreyi siler
async def delete_filter(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await is_admin(update, context):
        await update.message.reply_text('Bu komutu sadece yöneticiler kullanabilir.')
        return

    if len(context.args) < 1:
        await update.message.reply_text('Lütfen şu formatta girin: /deletefilter <kelime>')
        return

    keyword = context.args[0].lower()

    if keyword in filters_data:
        del filters_data[keyword]
        save_filters(filters_data)
        await update.message.reply_text(f'Filtre silindi: {keyword}')
    else:
        await update.message.reply_text(f'Filtre bulunamadı: {keyword}')


# Mesajları işleyen fonksiyon
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text.lower()
    filter_info = filters_data.get(user_message, None)

    if filter_info:
        response = filter_info['response']
        buttons = filter_info['buttons']

        # Gönderen kişinin adını al
        sender_name = f"{update.message.from_user.first_name} {update.message.from_user.last_name or ''}".strip()
        response = response.replace("{user_name}", sender_name)

        keyboard = [[InlineKeyboardButton(btn['text'], url=btn['url'])] for btn in buttons]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(response, reply_markup=reply_markup)


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    # Komutlar için handler'lar
    application.add_handler(CommandHandler('addfilter', add_filter))
    application.add_handler(CommandHandler('deletefilter', delete_filter))

    # Mesajları işlemek için handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()


if __name__ == '__main__':
    main()
