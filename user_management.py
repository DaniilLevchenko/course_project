"""
    User management.

    * - рекомендации
    ** - более сложные условия для высшего балла

        Основные возможности программы:
            - регистрация пользователей
            - просмотр учетных записей
            - хранение базы пользователей в течении сеанса
            ** хранение базы пользователей в файле
            ** сброс пароля пользователей
            ** удаление пользователей

        При запуске программы попадаем в "Главное меню":
            1. Зарегистрировать нового пользователя
            2. Просмотреть список пользователей

        При выборе пункта 1.
            - форма регистрации, аналогичная из hw5/reg_form.py, а именно:
                + ввод номера телефона
                + ввод email адреса
                + ввод и подтверждение пароля
            - номер телефона - уникальный (нельзя зарегистрировать двух пользователей с одинаковым номером телефона)
            - после успешной регистрации выводятся данные о пользователе и попадаем в Главное меню
            - данные о пользователе сохраняются:
                + в переменной
                + для хранения пользователей можно использовать любую структуру данных
                * использовать список словарей либо список объектов класса
                ** сохранять данные в файл (при перезапуске программы данные не теряются)

        При выборе пункта 2.
            - выводится количество зарегистрированных пользователей и
                задается вопрос: "Отобразить всех пользователей? (да/нет)"

                нет - попадаем в Главное меню
                да - переходим к следующему пункту

            - на экран выводится пронумерованный список пользователей (только номера телефонов)
            ** при выборе порядкового номера пользователя показывается детальная информация о пользователе
            ** после детальной информации выбор:
                1. Сбросить пароль
                    - пользователю генерируется новый случайный пароль
                    - отображается на экране
                    - возвращаемся в Главное меню
                2. Удалить пользователя
                    - * можно добавить подтверждение ("Вы действительно хотите удалить пользователя +380501234567? (да, нет)")
                    - возвращаемся в Главное меню

"""
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent


def main():
    while True:
        choice = input('1. Зарегистрировать нового пользователя\n2. Просмотреть список пользователей\n3. Выход из программы\n')
        if choice == '1':
            get_user_info()
        elif choice == '2':
            show_user_phone()
        elif choice == '3':
            print('Bye!')
            break


#1
def get_user_info():
    phone = get_phone()
    check_phone(phone)
    mail = email()
    password = gen_pass()
    save_data(phone, mail, password)
    print(
        f'Поздравляем с успешной регистрацией!\n'
        f'1. Ваш номер телефона: {phone}\n'
        f'2. Ваш эмейл: {mail}\n'
        f'3.Ваш пароль: {"*" * len(password)}')


#2
def email():
    mail = input('Enter your email: ')
    if len(mail) < 6:
        return email()
    elif mail.count('@') != 1:
        return email()
    return(mail)


#3
def gen_pass():
    password = input('Enter your password: ')
    counter_d = counter_l = counter_u = 0
    for char in password:
        if char.isdigit():
            counter_d += 1
        elif char.isupper():
            counter_u += 1
        elif char.islower():
            counter_l += 1
    if len(password) < 8:
        print('Пароль должен быть равен или длинее 8 символов.')
        return gen_pass() 
    if counter_l == 0 or counter_d == 0 or counter_u == 0:
        print('Пароль должен содержать минимум 1 строчную, 1 заглавную букву и 1 цифру.')
        return gen_pass()
    password_approve = input('Approve your password: ')
    if password_approve != password:
        print('Пароли не совпадают!')
        return gen_pass()
    return password

#4
def get_phone():
    phone = input('Enter phone number: ')
    edited_format = ''
    for char in phone:
        if char.isdigit():
            edited_format += char
    if len(edited_format) >= 9:
        edited_format = '380' + edited_format[-9:]
    elif len(edited_format) == 12:
        edited_format = edited_format
    elif len(edited_format) < 9:
        print('Цифр недостаточно.')
        return get_phone()
    return(edited_format)

#5
def save_data(phone, mail, password):
    with open(BASE_DIR / 'users.txt', 'a') as f:
        f.seek(0)
        f.write(f'{phone} {mail} {password}\n')

#6
def check_phone(phone):
    with open(BASE_DIR / 'users.txt', 'r') as f:
        for line in f:
            if phone in line:
                print('Данный номер уже зарегистрирован. Зарегистрируйте другой номер.')
                return get_phone()

#7
def show_user_phone():
    user_list()
    choice_info = input('Отобразить всех пользователей? yes/no: \n')
    if choice_info == 'yes':
        with open(BASE_DIR / 'users.txt', 'r') as f:
            n = 1
            f.seek(0)
            for line in f.readlines():
                user_phone = "".join(char for char in line if char.isdigit())
                user_phone = user_phone[:12]
                print(f'{n}. {user_phone}')
                n += 1
    elif choice_info == 'no':
        main()



def user_list():
    user_info_list = []
    count = 0
    with open(BASE_DIR / 'users.txt', 'r') as f:
        f.seek(0)
        for i in f.readlines():
            user_info_list.append(i[:-1])
            count += 1
        print(f'Кол-во зарегистрированных пользователей: {count}')
    return user_info_list


if __name__ == "__main__":
    main()