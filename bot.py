import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import telebot
from telebot import types

# Render uchun soxta server (Port xatosi bermasligi uchun)
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

# Asosiy menyu
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("⚠️ Yo'l belgilari")
    btn2 = types.KeyboardButton("📚 Qoidalar kitobi")
    btn3 = types.KeyboardButton("📝 Imtihon testlari")
    btn4 = types.KeyboardButton("💵 Jarimalar miqdori")
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    return markup

# Yo'l belgilari menyusi
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
    # Asosiy tugmalar
    if message.text == "⚠️ Yo'l belgilari":
        bot.send_message(message.chat.id, "Yo'l belgilari bo'limini tanlang:", reply_markup=belgilar_menu())
        
    elif message.text == "🔴 Taqiqlovchi belgilar":
        matn = (
            "**🔴 Taqiqlovchi belgilar (Asosiylari):**\n\n"
            "• **3.1 - Kirish taqiqlangan (Gisht):** Barcha transport vositalarining kirishini taqiqlaydi.\n"
            "• **3.2 - Harakatlanish taqiqlangan:** Barcha transport vositalarining harakatlanishini taqiqlaydi.\n"
            "• **3.24 - Yuqori tezlik cheklangan:** Belgida ko'rsatilganidan ortiq tezlikda harakatlanishni taqiqlaydi.\n"
            "• **3.27 - To'xtash taqiqlangan:** Transport vositalarining to'xtashi va to'xtab turishini taqiqlaydi."
        )
        bot.send_message(message.chat.id, matn, parse_mode="Markdown")
        
    elif message.text == "⚠️ Ogohlantiruvchi belgilar":
        matn = (
            "**⚠️ Ogohlantiruvchi belgilar (Asosiylari):**\n\n"
            "• **1.1 - Yo'l o'tkazgich:** Shlagbaumli temir yo'l o'tkazgichiga yaqinlashish.\n"
            "• **1.22 - Piyodalar o'tish joyi:** Piyodalar o'tish joyiga yaqinlashayotganingizni bildiradi.\n"
            "• **1.23 - Bolalar:** Yo'lning bolalar muassasalari yonidan o'tgan qismiga yaqinlashish.\n"
            "• **1.25 - Yo'l ishlari:** Yo mezonida ta'mirlash yoki qurilish ishlari olib borilmoqda."
        )
        bot.send_message(message.chat.id, matn, parse_mode="Markdown")

    elif message.text == "🔹 Imtiyozli belgilar":
        matn = (
            "**🔹 Imtiyozli (Avariyaviy) belgilar:**\n\n"
            "• **2.1 - Asosiy yo'l:** Haydovchiga tartibga solinmagan chorrahalardan birinchi bo'lib o'tish huquqini beradi.\n"
            "• **2.4 - Yo'l bering:** Haydovchi kesib o'tilayotgan yo'ldan harakatlanayotgan transportga yo'l berishi shart.\n"
            "• **2.5 - To'xtamay o'tish taqiqlangan (STOP):** To'xtash chizig'i yoki belgi oldida to'xtamasdan harakatlanish taqiqlanadi."
        )
        bot.send_message(message.chat.id, matn, parse_mode="Markdown")

    elif message.text == "⬅️ Ortga (Bosh menyu)":
        bot.send_message(message.chat.id, "Bosh menyuga qaytdingiz:", reply_markup=main_menu())

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
