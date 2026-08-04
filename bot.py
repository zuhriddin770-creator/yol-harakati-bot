import telebot
from telebot import types

# 🔴 DIQQAT: "TOKEN_KODINI_SHU_YERGA_YOZING" o'rniga @BotFather'dan olgan tokeningizni qo'ying!
BOT_TOKEN = "TOKEN_KODINI_SHU_YERGA_YOZING"
bot = telebot.TeleBot(BOT_TOKEN)

# 1. Foydalanuvchi botga kirib /start bosganida ishlaydigan bo'lim
@bot.message_handler(commands=['start'])
def welcome(message):
    # Bu yerda pastki menyu tugmalarini yaratamiz
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    btn1 = types.KeyboardButton("⚠️ Yo'l belgilari")
    btn2 = types.KeyboardButton("📚 Qoidalar kitobi")
    btn3 = types.KeyboardButton("📝 Imtihon testlari")
    btn4 = types.KeyboardButton("💵 Jarimalar miqdori")
    
    # Tugmalarni 2 qatorda joylashtiramiz (har bir qatorda 2 tadan)
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    
    # Foydalanuvchiga salom yo'llaymiz va tugmalarni ko'rsatamiz
    bot.send_message(
        message.chat.id, 
        f"Salom {message.from_user.first_name}! Yo'l harakati qoidalari botiga xush kelibsiz.\nQuyidagi bo'limlardan birini tanlang:", 
        reply_markup=markup
    )

# 2. Foydalanuvchi tugmalardan birini bosganda ishlaydigan bo'lim
@bot.message_handler(func=lambda message: True)
def handle_menu(message):
    if message.text == "⚠️ Yo'l belgilari":
        bot.send_message(message.chat.id, "Yaqinda bu yerga barcha yo'l belgilari (ogohlantiruvchi, taqiqlovchi va h.k.) qo'shiladi!")
        
    elif message.text == "📚 Qoidalar kitobi":
        bot.send_message(message.chat.id, "Bu bo'limda siz Yo'l harakati qoidalarining to'liq matnini o'qishingiz mumkin bo'ladi.")
        
    elif message.text == "📝 Imtihon testlari":
        bot.send_message(message.chat.id, "Bilimingizni sinash uchun testlar tizimi tez orada ishga tushadi.")
        
    elif message.text == "💵 Jarimalar miqdori":
        bot.send_message(message.chat.id, "Bu yerda eng ko'p uchraydigan qoidabuzarliklar va jarimalar ro'yxati bo'ladi.")

# 3. Bot o'chib qolmasdan, har soniyada yangi xabarlarni tekshirib turishi uchun buyruq
bot.infinity_polling()
