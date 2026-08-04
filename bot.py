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

# Belgilar ma'lumotlar bazasi (rasm va izohlari bilan)
ROAD_SIGNS = {
    "🛑 Taqiqlovchi belgilar": [
        {
            "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/3.1_Uzbekistan_road_sign.svg/500px-3.1_Uzbekistan_road_sign.svg.png",
            "caption": "🔴 *3.1 - Kirish taqiqlangan*\n\nUshbu yo'nalishda barcha transport vositalarining kirishi taqiqlanadi."
        },
        {
            "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/3.2_Uzbekistan_road_sign.svg/500px-3.2_Uzbekistan_road_sign.svg.png",
            "caption": "🚫 *3.2 - Harakatlanish taqiqlangan*\n\nBarcha transport vositalarining harakatlanishi taqiqlanadi."
        }
    ],
    "⚠️ Ogohlantiruvchi belgilar": [
        {
            "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/1.1_Uzbekistan_road_sign.svg/500px-1.1_Uzbekistan_road_sign.svg.png",
            "caption": "⚠️ *1.1 - Shlagbaumli temir yo'l o'tish joyi*\n\nOldinda shlagbaum bilan jihozlangan temir yo'l o'tish joyi borligini bildiradi."
        }
    ],
    "🔹 Imtiyozli belgilar": [
        {
            "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/2.1_Uzbekistan_road_sign.svg/500px-2.1_Uzbekistan_road_sign.svg.png",
            "caption": "🔷 *2.1 - Asosiy yo'l*\n\nHaydovchiga tartiblashtirilmagan chorrahalardan birinchi bo'lib o'tish huquqini beradi."
        }
    ]
}

# Menyular
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("⚠️ Yo'l belgilari"))
    return markup

def belgilar_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton("🛑 Taqiqlovchi belgilar")
    btn2 = types.KeyboardButton("⚠️ Ogohlantiruvchi belgilar")
    btn3 = types.KeyboardButton("🔹 Imtiyozli belgilar")
    btn4 = types.KeyboardButton("⬅️ Ortga (Bosh menyu)")
    markup.add(btn1, btn2, btn3, btn4)
    return markup

# Handlers
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        f"Assalomu alaykum, {message.from_user.first_name}!\nYo'l harakati qoidalari botiga xush kelibsiz!",
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda message: True)
def handle_all_messages(msg):
    text = msg.text

    if text == "⚠️ Yo'l belgilari":
        bot.send_message(msg.chat.id, "Yo'l belgilari bo'limini tanlang:", reply_markup=belgilar_menu())

    elif text in ROAD_SIGNS:
        # Tanlangan bo'limdagi barcha belgilarni rasm va matn bilan yuborish
        for sign in ROAD_SIGNS[text]:
            bot.send_photo(
                msg.chat.id,
                photo=sign["photo"],
                caption=sign["caption"],
                parse_mode="Markdown"
            )

    elif text == "⬅️ Ortga (Bosh menyu)":
        bot.send_message(msg.chat.id, "Bosh menyu:", reply_markup=main_menu())

bot.polling(none_stop=True)
