import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import telebot
from telebot import types

# Render port xatosini aylanib o'tish uchun soxta server
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

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("⚠️ Yo'l belgilari")
    btn2 = types.KeyboardButton("📚 Qoidalar kitobi")
    btn3 = types.KeyboardButton("📝 Imtihon testlari")
    btn4 = types.KeyboardButton("💵 Jarimalar miqdori")
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)

    bot.send_message(
        message.chat.id, 
        f"Assalomu alaykum, {message.from_user.first_name}!\nYo'l harakati qoidalari botiga xush kelibsiz!", 
        reply_markup=markup
    )

@bot.message_handler(content_types=['text'])
def handle_menu(message):
    if message.text == "⚠️ Yo'l belgilari":
        bot.send_message(message.chat.id, "Yaqinda bu yerga barcha yo'l belgilari qo'shiladi!")
    elif message.text == "📚 Qoidalar kitobi":
        bot.send_message(message.chat.id, "Yo'l harakati qoidalari kitobi tez orada yuklanadi.")
    elif message.text == "📝 Imtihon testlari":
        bot.send_message(message.chat.id, "Bilimingizni sinash uchun testlar tizimi tez orada ishga tushadi.")
    elif message.text == "💵 Jarimalar miqdori":
        jarimalar_matni = (
            "**Asosiy jarimalar miqdori:**\n\n"
            "• **Xavfsizlik kamari:** 187 500 so'm\n"
            "• **Telifonda gaplashish:** 1 125 000 so'm\n"
            "• **Qizil chiroqda o'tish:** 750 000 so'm\n"
            "• **Tezlikni oshirish (20 km/soatgacha):** 375 000 so'm\n"
            "• **Mast holatda rulga o'tish:** 9 375 000 so'm va 1.5 yildan 3 yilgacha haydash huquqidan mahrum qilish."
        )
        bot.send_message(message.chat.id, jarimalar_matni, parse_mode="Markdown")

bot.infinity_polling()
