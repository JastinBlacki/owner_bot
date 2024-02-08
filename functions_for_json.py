import json


def read_inf(file_name):
    with open(file_name, 'r', encoding="utf-8") as file:
        return json.load(file)


cars = read_inf("data/Cars.json")
companies = read_inf("data/Companies.json")
drivers = read_inf("data/Drivers.json")
sensors = read_inf("data/Sensors.json")
users = read_inf("data/Users.json")
defects = read_inf("data/Defects.json")
wheels = read_inf("data/Wheels.json")


def get_id_user_login(login):
    return [i.get('ID_user') for i in users if i.get('Login') == login][0]


def registered_users_login(type_):
    if type_ == "":
        log_users = [i.get("Login") for i in users]
    else:
        log_users = [i.get("Login") for i in users if i.get("Type") == type_]
    return log_users


def registered_users_password(type_):
    if type_ == "":
        pas_users = [i.get("Password") for i in users]
    else:
        pas_users = [i.get("Password") for i in users if i.get("Type") == type_]
    return pas_users


def get_inf_users(company_id, type_):
    return ([(i.get("ID_user"), i.get("Full name"), i.get("Birthday")) for i in users
             if i.get('Type') == type_ and i.get("Company") == company_id])


def get_car(inf, type_):
    return [i.get("Registration_number") for i in cars if int(i.get(type_)) == int(inf)]


def get_inf_car(id_car):
    return [(i.get('Registration_number'), i.get('Driver'), i.get('Brand')) for i in cars if i.get('Registration_number') in id_car]


def get_defects_driver_car(value, type_):
    return [(i.get("Type"), i.get("describe")) for i in defects if str(i.get(type_)) == str(value)]


def get_by_id(id_, inf):
    return [i.get(inf) for i in users if i.get("ID_user") == id_][0]


def get_id_df():
    b = json.load(open('data/Users.json', encoding='utf-8'))
    return b[len(b) - 1]['ID_user'] + 1


def add_row_json(dict_):
    b = json.load(open('data/Users.json', encoding='utf-8'))
    b.append(dict_)
    json.dump(b, open('data/Users.json', 'w'))


def get_id_driver_phone(login):
    return [i.get("ID_user") for i in users if str(i.get("Login")) == str(login)]


def delete_by_id(id_driver):
    del users[int(id_driver[0]) - 1]
    json.dump(users, open('data/Users.json', 'w'))

