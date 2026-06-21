import os
import telebot

# Railway-এর Environment Variable থেকে টোকেন নেবে, না থাকলে আপনার দেওয়া টোকেনটি ব্যবহার করবে
BOT_TOKEN = os.getenv("BOT_TOKEN", "8604217157:AAGRJrxh6RDsX6SEOfK7O3u1AJCjpuYlJ-Q")

bot = telebot.TeleBot(BOT_TOKEN)

# /start কমান্ড হ্যান্ডলার
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "MY NAME IS TANZID TAMIM")

# যেকোনো টেক্সট মেসেজের রিপ্লাই দেবে
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"আপনি বলেছেন: {message.text}")

print("Bot is running...")
bot.infinity_polling()
