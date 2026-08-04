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

# Yo'l belgilari ma'lumotlar bazasi
ROAD_SIGNS = {
    "taqiqlovchi": [
        {
            "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/3.1_Uzbekistan_road_sign.svg/320px-3.1_Uzbekistan_road_sign.svg.png",
            "caption": "🛑 <b>3.1 - Kirish taqiqlangan</b>\n\nUshbu yo'nalishda barcha transport vositalarining kirishi taqiqlanadi."
        },
        {
            "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/3.2_Uzbekistan_road_sign.svg/320px-3.2_Uzbekistan_road_sign.svg.png",
            "caption": "🚫 <b>3.2 - Harakatlanish taqiqlangan</b>\n\nBarcha transport vositalarining harakatlanishi taqiqlanadi."
        }
    ],
    "ogohlantiruvchi": [
        {
            "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/1.1_Uzbekistan_road_sign.svg/320px-1.1_Uzbekistan_road_sign.svg.png",
            "caption": "⚠️ <b>1.1 - Shlagbaumli temir yo'l o'tish joyi</b>\n\nOldinda shlagbaum bilan jihozlangan temir yo'l o'tish joyi borligini bildiradi."
        }
    ],
    "imtiyozli": [
        {
            "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/2.1_Uzbekistan_road_sign.svg/320px-2.1_Uzbekistan_road_sign.svg.png",
            "caption": "🔷 <b>2.1 - Asosiy yo'l</b>\n\nHaydovchiga tartiblashtirilmagan chorrahalardan birinchi bo'lib o'tish huquqini beradi."
        }
    ]
}

# Asosiy menyu
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("⚠️ Yo'l belgilari"))
    return markup

# Inline belgilar menyusi
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

# Matnli xabarlarni tutish
@bot.message_handler(func=lambda message: True)
def handle_text(msg):
    if "Yo'l belgilari" in msg.text:
        bot.send_message(
            msg.chat.id, 
            "Kerakli bo'limni tanlang:", 
            reply_markup=belgilar_inline_menu()
        )

# Inline tugma bosilganda javob qaytarish
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    category = call.data
    bot.answer_callback_query(call.id)  # Qotib qolmasligi uchun
    
    if category in ROAD_SIGNS:
        for sign in ROAD_SIGNS[category]:
            try:
                bot.send_photo(
                    call.message.chat.id,
                    photo=sign["photo"],
                    caption=sign["caption"],
                    parse_mode="HTML"
                )
            except Exception as e:
                # Agar rasm yuklanmay qolsa, matnning o'zini yuboradi
                bot.send_message(
                    call.message.chat.id,
                    f"{sign['caption']}\n\n<i>(Rasm yuklanmadi)</i>",
                    parse_mode="HTML"
                )

bot.polling(none_stop=True)
