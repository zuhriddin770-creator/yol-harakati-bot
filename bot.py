import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import telebot
from telebot import types

# Render uchun soxda server
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot ishlayapti")

def run_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

# Botni sozlash
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Belgilar bazasi (callback_data orqali bog'langan)
ROAD_SIGNS = {
    "taqiqlovchi": [
        {
            "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/3.1_Uzbekistan_road_sign.svg/500px-3.1_Uzbekistan_road_sign.svg.png",
            "caption": "🔴 *3.1 - Kirish taqiqlangan*\n\nUshbu yo'nalishda barcha transport vositalarining kirishi taqiqlanadi."
        },
        {
            "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/3.2_Uzbekistan_road_sign.svg/500px-3.2_Uzbekistan_road_sign.svg.png",
            "caption": "🚫 *3.2 - Harakatlanish taqiqlangan*\n\nBarcha transport vositalarining harakatlanishi taqiqlanadi."
        }
    ],
    "ogohlantiruvchi": [
        {
            "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/1.1_Uzbekistan_road_sign.svg/500px-1.1_Uzbekistan_road_sign.svg.png",
            "caption": "⚠️ *1.1 - Shlagbaumli temir yo'l o'tish joyi*\n\nOldinda shlagbaum bilan jihozlangan temir yo'l o'tish joyi borligini bildiradi."
        }
    ],
    "imtiyozli": [
        {
            "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/2.1_Uzbekistan_road_sign.svg/500px-2.1_Uzbekistan_road_sign.svg.png",
            "caption": "🔷 *2.1 - Asosiy yo'l*\n\nHaydovchiga tartiblashtirilmagan chorrahalardan birinchi bo'lib o'tish huquqini beradi."
        }
    ]
}

# 1. Asosiy menyu (Reply Keyboard)
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("⚠️ Yo'l belgilari"))
    return markup

# 2. Belgilar menyusi (Inline Keyboard - Xatosiz ishlaydi)
def belgilar_inline_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("🛑 Taqiqlovchi belgilar", callback_data="taqiqlovchi")
    btn2 = types.InlineKeyboardButton("⚠️ Ogohlantiruvchi belgilar", callback_data="ogohlantiruvchi")
    btn3 = types.InlineKeyboardButton("🔹 Imtiyozli belgilar", callback_data="imtiyozli")
    markup.add(btn1, btn2, btn3)
    return markup

# Handlers
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        f"Assalomu alaykum, {message.from_user.first_name}!\nYo'l harakati qoidalari botiga xush kelibsiz!",
        reply_markup=main_menu()
    )

# Text xabarlarni tutish
@bot.message_handler(func=lambda message: True)
def handle_text(msg):
    if "Yo'l belgilari" in msg.text:
        bot.send_message(
            msg.chat.id, 
            "Kerakli bo'limni tanlang:", 
            reply_markup=belgilar_inline_menu()
        )

# Inline tugmalar bosilganda rasmlarni yuborish
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    category = call.data
    if category in ROAD_SIGNS:
        # Tugma bosilganda Telegram'dagi soat belgisi yo'qolishi uchun
        bot.answer_callback_query(call.id)
        
        # Rasmlarni ketma-ket yuborish
        for sign in ROAD_SIGNS[category]:
            bot.send_photo(
                call.message.chat.id,
                photo=sign["photo"],
                caption=sign["caption"],
                parse_mode="Markdown"
            )

bot.polling(none_stop=True)
