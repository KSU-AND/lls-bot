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

def send_cmds(user_id, isnt_toss):
    if isnt_toss:
        bot.send_message(user_id, 
                        "Пока не была проведена жеребьевка ты можешь исправить "\
                        "свое имя, псевдоним и номер комнаты:\n"\
                        "/fix_name - исправить имя и фамилию\n"\
                        "/fix_nickname - исправить псевдоним\n"\
                        "/fix_room - исправить номер комнаты\n\n"\
                        "Также ты всегда можешь написать во всем вопросам @mendatsium.")
    else:
        bot.send_message(user_id, 
                         "Поскольку жеребьевка была уже проведена, то, к сожалению, "\
                         "исправить имя, псевдоним или номер комнаты уже не получиться.\n\n"\
                         "Но ты всегда можешь написать во всем вопросам @mendatsium.")