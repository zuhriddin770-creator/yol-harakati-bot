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
        self.wfile.write(b"Bot ishlayapti!")

def run_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

# Bot kodi
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("⚠️ Yo'l belgilari")
    btn2 = types.KeyboardButton("📚 Qoidalar kitobi")
    btn3 = types.KeyboardButton("📝 Imtihon testlari")
    btn4 = types.KeyboardButton("💵 Jarimalar miqdori")
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    return markup

def belgilar_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🔴 Taqiqlovchi belgilar")
    btn2 = types.KeyboardButton("⚠️ Ogohlantiruvchi belgilar")
    btn3 = types.KeyboardButton("🔹 Imtiyozli belgilar")
    btn4 = types.KeyboardButton("⬅️ Ortga (Bosh menyu)")
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    markup.add(btn4)
    return markup

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(
        message.chat.id, 
        f"Assalomu alaykum, {message.from_user.first_name}!\nYo'l harakati qoidalari botiga xush kelibsiz!", 
        reply_markup=main_menu()
    )

@bot.message_handler(content_types=['text'])
def handle_menu(message):
    if message.text == "⚠️ Yo'l belgilari":
        bot.send_message(message.chat.id, "Yo'l belgilari bo'limini tanlang:", reply_markup=belgilar_menu())
        
    elif message.text == "🔴 Taqiqlovchi belgilar":
        photo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Road_sign_3.1.svg/500px-Road_sign_3.1.svg.png"
        caption = "<b>3.1 - Kirish taqiqlangan ('G'isht')</b>\n\nBarcha transport vositalarining kirishini taqiqlaydi."
        bot.send_photo(message.chat.id, photo_url, caption=caption, parse_mode="HTML")
        
    elif message.text == "⚠️ Ogohlantiruvchi belgilar":
        photo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Road_sign_1.22.svg/500px-Road_sign_1.22.svg.png"
        caption = "<b>1.22 - Piyodalar o'tish joyi</b>\n\nPiyodalar o'tish joyiga yaqinlashayotganingiz haqida ogohlantiradi."
        bot.send_photo(message.chat.id, photo_url, caption=caption, parse_mode="HTML")

    elif message.text == "🔹 Imtiyozli belgilar":
        photo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Road_sign_2.5.svg/500px-Road_sign_2.5.svg.png"
        caption = "<b>2.5 - To'xtamay o'tish taqiqlangan (STOP)</b>\n\nTo'xtash chizig'i yoki belgi oldida to'xtamasdan harakatlanish taqiqlanadi."
        bot.send_photo(message.chat.id, photo_url, caption=caption, parse_mode="HTML")

    elif message.text == "⬅️ Ortga (Bosh menyu)":
        bot.send_message(message.chat.id, "Bosh menyuga qaytdingiz:", reply_markup=main_menu())

    elif message.text == "📚 Qoidalar kitobi":
        bot.send_message(message.chat.id, "Yo'l harakati qoidalari kitobi tez orada yuklanadi.")
        
    elif message.text == "📝 Imtihon testlari":
        bot.send_message(message.chat.id, "Bilimingizni sinash uchun testlar tizimi tez orada ishga tushadi.")
        
    elif message.text == "💵 Jarimalar miqdori":
        jarimalar_matni = (
            "<b>Asosiy jarimalar miqdori:</b>\n\n"
            "• <b>Xavfsizlik kamari:</b> 187 500 so'm\n"
            "• <b>Telifonda gaplashish:</b> 1 125 000 so'm\n"
            "• <b>Qizil chiroqda o'tish:</b> 750 000 so'm\n"
            "• <b>Tezlikni oshirish:</b> 375 000 so'm"
        )
        bot.send_message(message.chat.id, jarimalar_matni, parse_mode="HTML")

bot.infinity_polling()
