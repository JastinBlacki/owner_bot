import telebot
from telebot import types
from functions_for_json import *

token = '6821919054:AAGcj-d94HKSl8REdyJzRI-ahCmTDJDol-8'
bot = telebot.TeleBot(token)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    call_funk = callback.data
    message = callback.message

    match call_funk:
        case 'sign_in':
            sign_in(message)
        case 'all_drivers':
            get_all_drivers(message)
        case 'car':
            get_all_cars(message)
        case 'add_driver':
            add_drivers(message)
        case 'delete_driver':
            delete_driver(message)


@bot.message_handler(commands=['start'])
def start_message(message):

    chat_id = message.chat.id

    deleter(message)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Войти в систему', callback_data='sign_in'))
    bot.send_message(chat_id, '🔐 <b>Войти</b> в систему для <u>старта</u>.', reply_markup=markup, parse_mode='html')


    # deleter(message)
    # bot.send_message(message.chat.id,
    #                  "Напишите свой номер телефона в виде - '+79999999999' для регистрации")
    # bot.register_next_step_handler(message, is_registered)


@bot.message_handler(commands=['sign_out'])
def out_message(message):
    chat_id = message.chat.id

    deleter(message)

    if is_sign_in(chat_id):
        del_user_log(chat_id)
        bot.send_message(chat_id, "🚪 <b>Сессия завершена.</b>\n", parse_mode='html')


def sign_in(message):
    chat_id = message.chat.id

    # add_message(message)  # Добавление сообщения, которое ввёл пользователь

    if not is_sign_in(chat_id):
        bot.send_message(chat_id, "💼 <b>Введите</b> логин компании.", parse_mode='html')
        bot.register_next_step_handler(message, is_registered)
    else:
        login = get_login(message.chat.id)
        id_owner = get_id_user_login(login)
        global owner
        # экземпляр класса со всей инфой о текущем пользователе
        owner = Owner(id_owner, get_by_id(id_owner, "Full name"), get_by_id(id_owner, "Company"))
        help_message(message)


def is_registered(message):
    chat_id = message.chat.id
    registered_drivers = registered_users_login('Владелец')

    login = str(message.text)

    if login in registered_drivers:
        id_owner = get_id_user_login(message.text)
        global owner
        # экземпляр класса со всей инфой о текущем пользователе
        owner = Owner(id_owner, get_by_id(id_owner, "Full name"), get_by_id(id_owner, "Company"))
        bot.send_message(chat_id, "Введите пароль")
        bot.register_next_step_handler(message, pass_login_drivers, login=login)
    else:
        bot.send_message(chat_id, "Вашего номера телефона не найдено в базе данных.")
        start_message(message)


def pass_login_drivers(message, login):
    password_drivers = registered_users_password("Владелец")
    if str(message.text) in password_drivers:
        bot.send_message(message.chat.id, 'Вы успешно вошли в аккаунт')
        add_user_log(message.chat.id, login)
        help_message(message)
    
        # bot.send_message(message.chat.id, "Для просмотра всех функций введите /help")


@bot.message_handler(commands=['main_menu'])
def help_message(message):
    deleter(message)

    if is_sign_in(message.chat.id):
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('⚙️ Все водители компании', callback_data='all_drivers')
        btn2 = types.InlineKeyboardButton('🏢 Все машины компании', callback_data='car')
        markup.row(btn1, btn2)
        btn3 = types.InlineKeyboardButton('🚘 Добавить водителя', callback_data='add_driver')
        btn4 = types.InlineKeyboardButton('🚗 Удалить водителя', callback_data='delete_driver')
        markup.row(btn3, btn4)

        bot.send_message(message.chat.id, "Все водители компании - /all_drivers\n"
                                        "Все машины компании - /car\n"
                                        "Добавить водителя - /add_driver\n"
                                        "Удалить водителя - /delete_driver", reply_markup=markup)
    else:
        start_message(message)


# получить всех водителей компании владельца
@bot.message_handler(commands=['all_drivers'])
def get_all_drivers(message):
    deleter(message)
    res = ""
    for i in get_inf_users(owner.company, "Водитель"):
        res += "ФИО = " + i[1] + " Дата рождения = " + i[2] + "\n"
    bot.send_message(message.chat.id, res)
    help_message(message)


# получить все машины компании владельца
@bot.message_handler(commands=['car'])
def get_all_cars(message):
    deleter(message)
    car_id = get_car(owner.company, "Company")
    res = ""
    for i in get_inf_car(car_id):
        res += "Регистрационный номер = " + str(i[1]) + " Марка = " + str(i[2]) + "\n"
    bot.send_message(message.chat.id, res)
    help_message(message)


@bot.message_handler(commands=['add_driver'])
def add_drivers(message):
    deleter(message)
    bot.send_message(message.chat.id, "Введите информацию о водителе в следующем форте: "
                                      "Номер телефона, пароль, имя, день рождения (ДД.ММ.ГГГГ)")
    bot.register_next_step_handler(message, add_drivers_json)


@bot.message_handler(commands=['delete_driver'])
def delete_driver(message):
    deleter(message)
    bot.send_message(message.chat.id, "Введите телефонный номер водителя, которого хотите удалить")
    bot.register_next_step_handler(message, delete_driver_json)


def delete_driver_json(message):
    try:                                                                                                                                                                                                                                
        id_driver = get_id_driver_phone(message.text)
        delete_by_id(id_driver)
    except Exception:
        bot.send_message(message.chat.id, f'Данные водителя: {message.text} - не соответствуют форме.')
        help_message(message)


# добавление пользователя (записываем всю инфу в словарь)
def add_drivers_json(message):
    id_ = get_id_df()
    try:
        login, password, name, birthday = message.text.split(", ")
        driver_ = {"ID_user": id_, "Type": "Водитель", "Login": login, "Password": password,
                "Full name": name, "Company": owner.company, "Birthday": birthday}
        add_row_json(driver_)
        bot.send_message(message.chat.id, "Водитель добавлен")
    except Exception:
        bot.send_message(message.chat.id, f'Данные водителя: {message.text} - не соответствуют форме.')



# получить дефекты опред.пользователя (тип отчет), но оно пока нигде не используется, просто функция
def get_defects(message):
    mes_ = ""
    report_ = get_defects_driver_car(str(message.text), 'driver_id')
    for i in report_:
        mes_ += "Тип поломки: " + i[0]
        mes_ += "\nОписание поломки: " + i[1] + "\n"
    bot.send_message(message.chat.id, mes_)


@bot.message_handler(func=lambda message: message)
def deleter(message):
    chat_id = message.chat.id
    deleter_message(chat_id, message, 10)


def deleter_message(chat_id, message, count_del=1):
    message_id = message.id
    if count_del < 0:
        del_list = range(0, count_del, -1)
    else:
        del_list = range(count_del)

    for i in del_list:
        try:
            bot.delete_message(chat_id, message_id-i)
        except Exception:
            continue


class Owner:
    def __init__(self, id_, name, company):
        self.id_ = id_
        self.name = name
        self.company = company


bot.infinity_polling()
