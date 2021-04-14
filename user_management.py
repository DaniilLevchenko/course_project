import random
import string
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent


def main():
    while True:
        choice = input(
            f'\n1. Зарегистрировать нового пользователя\n'
            f'2. Просмотреть список пользователей\n'
            f'3. Выход из программы\n')
        if choice == '1':
            get_user_info()
        elif choice == '2':
            show_user()
        elif choice == '3':
            print('\nПока!')
            break


def get_user_info():
    phone = phone_valid()
    check_phone(phone)
    mail = get_email()
    password = get_pass()
    save_data(phone, mail, password)
    print(
        f'\nПоздравляем с успешной регистрацией!\n'
        f'1. Ваш номер телефона: {phone}\n'
        f'2. Ваш эмейл: {mail}\n'
        f'3. Ваш пароль: {"*" * len(password)}')


def is_valid_email(mail):
    if len(mail) < 6:
        return False
    elif mail.count('@') != 1:
        return False
    return mail


def is_valid_pass(password):
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
        return False
    if counter_l == 0 or counter_d == 0 or counter_u == 0:
        print('Пароль должен содержать минимум 1 строчную, 1 заглавную букву и 1 цифру.')
        return False
    password_approve = input('Подтвердите пароль: ')
    if password_approve != password:
        print('Пароли не совпадают!')
        return False
    return True


def phone_valid():
    phone = input('Введите Ваш номер телефона: ')
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
        return phone_valid()
    return edited_format


def get_email():
    mail = input('Введите эмейл: ')
    if is_valid_email(mail):
        return mail
    else:
        return get_email()


def get_pass():
    password = input('Введите пароль: ')
    if is_valid_pass(password):
        return password
    else:
        return get_pass()


def save_data(phone, mail, password):
    with open(BASE_DIR / 'users.txt', 'a') as f:
        f.seek(0)
        f.write(f'{phone} {mail} {password}\n')


def check_phone(phone):
    with open(BASE_DIR / 'users.txt', 'r') as f:
        for line in f:
            if phone in line:
                print('Данный номер уже зарегистрирован. Зарегистрируйте другой номер.')
                return phone_valid()

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


def show_user():
    user_list()
    choice_info = input('Отобразить всех пользователей? yes/no: \n')
    if choice_info == 'yes':
        show_phone()
        show_info()
    elif choice_info == 'no':
        main()


def show_phone():
    with open(BASE_DIR / 'users.txt', 'r') as f:
            n = 1
            f.seek(0)
            for line in f.readlines():
                user_phone = "".join(char for char in line if char.isdigit())
                user_phone = user_phone[:12]
                print(f'\n{n}. {user_phone}')
                n += 1
    return


def show_info():
    n = int(input('Выберите порядковый номер пользователя: '))
    n -= 1
    with open(BASE_DIR / 'users.txt', 'r') as f:
        f.seek(0)
        info = f.readlines()
        print(f'\n{info[n]}')
    return user_operations(n)


def user_operations(n):
    choice = input(
        f'1.Сбросить пароль\n'
        f'2.Удалить пользователя\n'
        f'3.Вернуться в главное меню\n')
    if choice == '1':
        generate_pass(n)
    elif choice == '2':
        delete_user(n)
    elif choice == '3':
        return


def generate_pass(n):
    with open(BASE_DIR / 'users.txt', 'r') as f:
        data = f.readlines()
    d = data[n]
    d = d.split(' ')
    d.pop()
    new_password = strong_pass_gen()
    new_password = ''.join(new_password)
    print(f'\nВаш новый пароль: {new_password}')
    d.append(new_password)
    data[n] = ' '.join(d)
    with open(BASE_DIR / "users.txt", "w") as f:
        for lines in data:
            f.write(lines)
    return


def strong_pass_gen():
    counter_l = counter_u = counter_d = 0
    p = string.ascii_lowercase + string.ascii_uppercase + string.digits
    password = random.sample(p, random.randint(8,16))
    for char in password:
        if char.islower():
            counter_l += 1
        elif char.isupper():
            counter_u += 1
        elif char.isdigit():
            counter_d += 1
    if counter_l > 0 and counter_u > 0 and counter_d > 0:
        return password


def delete_user(n):
    with open(BASE_DIR / 'users.txt', 'r') as f:
        data = f.readlines()
        d = data[n]
    with open(BASE_DIR / "users.txt", "w") as f:
        for line in data:
            if line != d:
                f.write(line)
    print(f'\nПользователь удалён.\n')


if __name__ == "__main__":
    main()