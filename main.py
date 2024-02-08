import telebot
from telebot import types
from functions_for_json import *

token = '6878346739:AAGPR-088yImPStl8Ss64UhxgR0ka0gpa1Q'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,
                     "Здравствуй,  напиши свой номер телефона в виде - '+79999999999' для регистрации")
    bot.register_next_step_handler(message, is_registered)


def is_registered(message):
    chat_id = message.chat.id
    registered_drivers = registered_users_login('Владелец')
    if str(message.text) in registered_drivers:
        id_owner = get_id_user_login(message.text)
        global owner
        # экземпляр класса со всей инфой о текущем пользователе
        owner = Owner(id_owner, get_by_id(id_owner, "Full name"), get_by_id(id_owner, "Company"))
        bot.send_message(chat_id, "Введите пароль")
        bot.register_next_step_handler(message, pass_login_drivers)
    else:
        bot.send_message(chat_id, "Вашего номера телефона не найдено в базе данных.")


def pass_login_drivers(message):
    password_drivers = registered_users_password("Владелец")
    if str(message.text) in password_drivers:
        bot.send_message(message.chat.id, 'Вы успешно вошли в аккаунт')
        bot.send_message(message.chat.id, "Для просмотра всех функций введите /help")


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, "Все водители компании - /all_drivers)\n"
                                      "Все машины компании - /car\n"
                                      "Добавить водителя - /add_driver\n"
                                      "Удалить водителя - /delete_driver")


# получить всех водителей компании владельца
@bot.message_handler(commands=['all_drivers'])
def get_all_drivers(message):
    res = ""
    for i in get_inf_users(owner.company, "Водитель"):
        res += "ФИО = " + i[1] + " Дата рождения = " + i[2] + "\n"
    bot.send_message(message.chat.id, res)


# получить все машины компании владельца
@bot.message_handler(commands=['car'])
def get_all_cars(message):
    car_id = get_car(owner.company, "Company")
    res = ""
    for i in get_inf_car(car_id):
        res += "Регистрационный номер = " + str(i[1]) + " Марка = " + str(i[2]) + "\n"
    bot.send_message(message.chat.id, res)


@bot.message_handler(commands=['add_driver'])
def add_drivers(message):
    bot.send_message(message.chat.id, "Введите информацию о водителе в следующем форте: "
                                      "Номер телефона, пароль, имя, день рождения (ДД.ММ.ГГГГ)")
    bot.register_next_step_handler(message, add_drivers_json)


@bot.message_handler(commands=['delete_driver'])
def delete_driver(message):
    bot.send_message(message.chat.id, "Введите телефонный номер водителя, которого хотите удалить")
    bot.register_next_step_handler(message, delete_driver_json)


def delete_driver_json(message):
    id_driver = get_id_driver_phone(message.text)
    delete_by_id(id_driver)


# добавление пользователя (записываем всю инфу в словарь)
def add_drivers_json(message):
    id_ = get_id_df()
    login, password, name, birthday = message.text.split(", ")
    driver_ = {"ID_user": id_, "Type": "Водитель", "Login": login, "Password": password,
               "Full name": name, "Company": owner.company, "Birthday": birthday}
    add_row_json(driver_)
    bot.send_message(message.chat.id, "Водитель добавлен")


# получить дефекты опред.пользователя (тип отчет), но оно пока нигде не используется, просто функция
def get_defects(message):
    mes_ = ""
    report_ = get_defects_driver_car(str(message.text), 'driver_id')
    for i in report_:
        mes_ += "Тип поломки: " + i[0]
        mes_ += "\nОписание поломки: " + i[1] + "\n"
    bot.send_message(message.chat.id, mes_)


class Owner:
    def __init__(self, id_, name, company):
        self.id_ = id_
        self.name = name
        self.company = company


bot.infinity_polling()
