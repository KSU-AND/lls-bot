import telebot
from telebot import types
import mysecrets

bot = telebot.TeleBot(mysecrets.BOT_TOKEN)

def create_markup(*button_names):
    num_of_buttons = len(button_names)
    if num_of_buttons == 0:
        return types.ReplyKeyboardRemove()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for button_name in button_names:
        keyboard.add(types.KeyboardButton(button_name))
    return keyboard

def send_full_csv_file(user_id):
    with open("full_DB.csv", "rb") as csv_file:
        bot.send_document(user_id, csv_file)