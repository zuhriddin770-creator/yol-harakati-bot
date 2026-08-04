import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import telebot
from telebot import types

# Render uchun soxta server
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

# Yo'l belgilari bazasi (Ishochnli rasmlar havolasi bilan)
ROAD_SIGNS = {
    "taqiqlovchi": [
        {
            "photo": "https://raw.githubusercontent.com/yol-belgilari/images/main/3_1.png",
            "caption": "🛑 <b>3.1 - Kirish taqiqlangan</b>\n\nUshbu yo'nalishda barcha transport vositalarining kirishi taqiqlanadi."
        },
        {
            "photo": "https://raw.githubusercontent.com/yol-belgilari/images/main/3_2.png",
            "caption": "🚫 <b>3.2 - Harakatlanish taqiqlangan</b>\n\nBarcha transport vositalarining harakatlanishi taqiqlanadi."
        }
    ],
    "ogohlantiruvchi": [
        {
            "photo": "https://raw.githubusercontent.com/yol-belgilari/images/main/1_1.png",
            "caption": "⚠️ <b>1.1 - Shlagbaumli temir yo'l o'tish joyi</b>\n\nOldinda shlagbaum bilan jihozlangan temir yo'l o'tish joyi borligini bildiradi."
        }
    ],
    "imtiyozli": [
        {
            "photo": "https://raw.githubusercontent.com/yol-belgilari/images/main/2_1.png",
            "caption": "🔷 <b>2.1 - Asosiy yo'l</b>\n\nHaydovchiga tartiblashtirilmagan chorrahalardan birinchi bo'lib o'tish huquqini beradi."
        }
    ]
}

# 1. BOSH MENYU (Oldingi barcha tugmalar qaytarildi)
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("⚠️ Yo'l belgilari")
    btn2 = types.KeyboardButton("📚 Qoidalar")
    btn3 = types.KeyboardButton("📝 Imtihon")
    btn4 = types.KeyboardButton("💵 Jarimalar")
    markup.add(btn1, btn2, btn3, btn4)
    return markup

# 2. BELGILAR MENYUSI
def belgilar_inline_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🛑 Taqiqlovchi belgilar", callback_data="taqiqlovchi"),
        types.InlineKeyboardButton("⚠️ Ogohlantiruvchi belgilar", callback_data="ogohlantiruvchi"),
        types.InlineKeyboardButton("🔹 Imtiyozli belgilar", callback_data="imtiyozli")
    )
    return markup

# /start buyrug'i
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        f"Assalomu alaykum, {message.from_user.first_name}!\nYo'l harakati qoidalari botiga xush kelibsiz!",
        reply_markup=main_menu()
    )

# Matnli xabar ishlovchisi
@bot.message_handler(func=lambda message: True)
def handle_text(msg):
    text = msg.text
    if "Yo'l belgilari" in text:
        bot.send_message(msg.chat.id, "Kerakli bo'limni tanlang:", reply_markup=belgilar_inline_menu())
    elif "Qoidalar" in text:
        bot.send_message(msg.chat.id, "📚 Yo'l harakati qoidalari bo'limi tez orada qo'shiladi.")
    elif "Imtihon" in text:
        bot.send_message(msg.chat.id, "📝 Imtihon va testlar bo'limi tez orada qo'shiladi.")
    elif "Jarimalar" in text:
        bot.send_message(msg.chat.id, "💵 Jarimalar miqdori bo'limi tez orada qo'shiladi.")

# Inline tugmalarga javob berish
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    category = call.data
    bot.answer_callback_query(call.id)
    
    if category in ROAD_SIGNS:
        for sign in ROAD_SIGNS[category]:
            # Rasmni yuborib ko'ramiz
            try:
                bot.send_photo(
                    call.message.chat.id,
                    photo=sign["photo"],
                    caption=sign["caption"],
                    parse_mode="HTML"
                )
            except Exception:
                # Agar havola ishlamasa, zaxira usul bilan yuboradi
                bot.send_message(
                    call.message.chat.id,
                    sign["caption"],
                    parse_mode="HTML"
                )

bot.polling(none_stop=True)
