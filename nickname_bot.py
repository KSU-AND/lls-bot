from enums4bot import *
from BOT_functions import *
from DB_functions import *
import mysecrets

@bot.message_handler(commands=["start"])
def cmd_start(message):
    user_id = message.chat.id

    if not check_user_in_db(user_id) or check_role_is_null(user_id): # TODO #26
        bot.send_message(user_id, 
                         "Добрый день! "\
                         "Для начала давайте определимся, кто Вы?",  
                         reply_markup = create_markup(Answers.STUDENT.value,
                                                      Answers.ADMIN.value))
        add_user(user_id)
        set_state(user_id, States.U_ROLE)
        print(f"Пользователь id_{user_id} добавлен в базу.")

    elif get_role(user_id) != Roles.STUDENT.value: # TODO #27
        set_state(user_id, States.A_CODE)
        bot.send_message(user_id, 
                         "Введите подтверждающий код:\n", 
                         reply_markup = create_markup())
        print(f"Пользователь id_{user_id} пытается ввести код.")

    elif not get_name(user_id): # TODO #29
        set_state(user_id, States.S_NAME)
        bot.send_message(user_id, 
                         "Введи, пожалуйста, свои фамилию и имя.\n"\
                         "(Их будут видеть организаторы и почтальон)", 
                         reply_markup = create_markup())

    elif check_nickname_is_null(user_id): # TODO #28
        set_state(user_id, States.S_NICKNAME)
        bot.send_message(user_id, 
                         f"Привет, {get_name(user_id)}! \n"\
                         "Придумай и введи свой псевдоним:", 
                         reply_markup = create_markup())
    else:
        set_state(user_id, States.S_FULL)
        bot.send_message(user_id, 
                         f"Привет, {get_name(user_id)}! \n"\
                         "Я могу напомнить тебе твой псевдоним или подсказать, "\
                         "какой псевдоним у твоего друга по переписке (если жеребьевка уже была проведена)", 
                         reply_markup = create_markup(Answers.NICKNAME.value,
                                                      Answers.FRIEND.value))

@bot.message_handler(func=lambda message: get_state(message.chat.id) == States.U_ROLE)
def user_entered_role(message):
    user_id = message.chat.id
    msg_text = message.text.strip()
    
    if msg_text == Answers.STUDENT.value:
        set_state(user_id, States.S_NAME)
        set_role(user_id, Roles.STUDENT.value) 

        bot.send_message(user_id, 
                         "Отлично! \n"\
                         "Теперь давай познакомимся поближе: введи, пожалуйста, свои фамилию и имя.\n"\
                         "(Их будут видеть организаторы и почтальон)", 
                         reply_markup = create_markup())
        print(f"Пользователю id_{user_id} поставлена роль {Roles.STUDENT.value}.")
    elif msg_text == Answers.ADMIN.value:
        set_state(user_id, States.A_CODE)
        bot.send_message(user_id, 
                         "Введите подтверждающий код:\n", 
                         reply_markup = create_markup())
        print(f"Пользователь id_{user_id} пытается ввести код.")
    else:
        bot.send_message(user_id, "Выберете, пожалуйста, одну из двух кнопок.")

@bot.message_handler(func=lambda message: get_state(message.chat.id) == States.S_NAME)
def user_entered_name(message):
    user_id = message.chat.id
    msg_text = message.text.strip()

    set_state(user_id, States.S_NICKNAME)
    set_name(user_id, msg_text) 
    bot.send_message(user_id, 
                         "Приятно познакомиться! \n"\
                         "Теперь придумай и введи свой псевдоним:", 
                         reply_markup = create_markup())
    print(f"Пользователь id_{user_id} зарегистрировался как {msg_text}.")

@bot.message_handler(func=lambda message: get_state(message.chat.id) == States.S_NICKNAME)
def user_entered_nickname(message):
    user_id = message.chat.id
    msg_text = message.text.strip()

    if check_nickname_in_db(msg_text):
        bot.send_message(user_id, 
                         "К сожалению, такой псевдоним уже есть. Придумай что-то другое.", 
                         reply_markup = create_markup())
    else:
        set_state(user_id, States.S_ROOM)
        set_nickname(user_id, msg_text) 
        bot.send_message(user_id, 
                         "Принято! \n"\
                         "И остался последний шаг. Введи, пожалуйста, номер своей комнаты.", 
                         reply_markup = create_markup())
        print(f"Пользователь {get_name(user_id)} ввел псевдоним {msg_text}.")

@bot.message_handler(func=lambda message: get_state(message.chat.id) == States.S_ROOM)
def user_entered_room(message):
    user_id = message.chat.id
    msg_text = message.text.strip()

    set_state(user_id, States.S_FULL)
    set_room(user_id, msg_text) 
    bot.send_message(user_id, 
                        "Принято! \n"\
                        "Если забудешь свой псевдоним, можешь вернуться ко мне в любой "\
                        "момент и я его тебе напомню. Узнать своего собеседника после "\
                        "проведения жеребьевки тоже можно будет здесь.", 
                        reply_markup = create_markup(Answers.NICKNAME.value,
                                                    Answers.FRIEND.value))
    print(f"Пользователь {get_name(user_id)} ввел номер комнаты {msg_text}.")

@bot.message_handler(func=lambda message: get_state(message.chat.id) == States.A_CODE)
def user_entered_code(message):
    user_id = message.chat.id
    msg_text = message.text.strip()

    if msg_text == mysecrets.ADMIN_PASSWORD:
        set_state(user_id, States.A_FULL)
        set_role(user_id, Roles.ADMIN.value)
        bot.send_message(user_id, 
                         "Правильный код! \n"\
                         "Вы можете узнать общее количество зарегистировавшихся на данный момент, "\
                         "провести жеребьевку среди участников или скачать документ со всеми данными "\
                         "(имя, пседвоним и собеседник каждого участника).", 
                         reply_markup = create_markup(Answers.TOTAL.value,
                                                      Answers.TOSS.value,
                                                      Answers.DOC.value))
        print(f"Пользователь id_{user_id} ввел правильный код, ему присваевается роль {Roles.ADMIN.value}.")
    else:
        bot.send_message(user_id, 
                         "Неправильный код. Попробуйте еще раз:", 
                         reply_markup = create_markup())
        print(f"Пользователь id_{user_id} неправильно ввел код.")

@bot.message_handler(func=lambda message: get_state(message.chat.id) == States.S_FULL)
def student_wants(message):
    user_id = message.chat.id
    msg_text = message.text.strip()

    if msg_text == Answers.NICKNAME.value:
        bot.send_message(user_id, 
                         f"Твой псевдоним: {get_nickname(user_id)}",
                         parse_mode="MarkdownV2",
                         reply_markup = create_markup(Answers.NICKNAME.value,
                                                      Answers.FRIEND.value))
        print(f"Пользователь {get_name(user_id)} попросил напомнить псевдоним и получил его.")
    elif msg_text == Answers.FRIEND.value: # TODO #33
        friend = get_friend(user_id)
        if friend:
            friend = get_nickname(friend)
            bot.send_message(user_id, 
                         f"Псевдоним твоего собеседника: `{friend}`",
                         parse_mode="MarkdownV2",
                         reply_markup = create_markup(Answers.NICKNAME.value,
                                                      Answers.FRIEND.value))
            print(f"Пользователь {get_name(user_id)} попросил псевдоним друга и получил его.")
        else:
            bot.send_message(user_id, 
                         f"Жеребьевка еще не была проведена. Спроси у меня позже", 
                         reply_markup = create_markup(Answers.NICKNAME.value,
                                                      Answers.FRIEND.value))
            print(f"Пользователь {get_name(user_id)} попросил псевдоним друга, но жеребьевки еще не было.")

@bot.message_handler(func=lambda message: get_state(message.chat.id) == States.A_FULL)
def admin_wants(message):
    user_id = message.chat.id
    msg_text = message.text.strip()

    if msg_text == Answers.TOTAL.value:
        bot.send_message(user_id, 
                         f"Общее количество участников на данный момент: {get_total_students()}",
                         reply_markup = create_markup(Answers.TOTAL.value,
                                                      Answers.TOSS.value,
                                                      Answers.DOC.value))
        print(f"admin_{user_id} запросил общее кол-во участников и получил его.")
    elif msg_text == Answers.TOSS.value:
        if not toss_is_able():
            bot.send_message(user_id, 
                         f"Жеребьевка уже была проведена.",
                         reply_markup = create_markup(Answers.TOTAL.value,
                                                      Answers.TOSS.value,
                                                      Answers.DOC.value))
            print(f"admin_{user_id} попытался повторно провести жеребьевку.")
        elif get_total_students() % 2:
            bot.send_message(user_id, 
                         "В данный момент зарегистрировано нечетное количество "\
                         f"участников ({get_total_students()}). Жеребьевка не может быть проведена, "\
                         "пока количество участников не будет четным.",
                         reply_markup = create_markup(Answers.TOTAL.value,
                                                      Answers.TOSS.value,
                                                      Answers.DOC.value))
            print(f"admin_{user_id} попытался провести жеребьевку и не преуспел.")
        else:
            create_toss()
            bot.send_message(user_id, 
                         f"Поздравляю, вы провели жеребьевку! Всю информацию можно "\
                         "увидеть в общем файле.",
                         reply_markup = create_markup(Answers.TOTAL.value,
                                                      Answers.TOSS.value,
                                                      Answers.DOC.value))
            print(f"admin_{user_id} успешно провел жеребьевку.")
    elif msg_text == Answers.DOC.value:
        create_full_csv_file()
        send_full_csv_file(user_id)
        print(f"admin_{user_id} запросил общий файл с базой и получил его.")


if __name__ == "__main__":
    bot.infinity_polling(timeout = 10, long_polling_timeout = 5) # почему-то везде рекомендуют такие значения