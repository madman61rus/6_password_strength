import argparse
import os
import re

def check_blacklist(file_path, password):
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r', encoding='utf-8') as data_file:
        blacklisted_keys = data_file.read().split()
        data_file.close()
        return password in blacklisted_keys

def check_password_length(password):
    return len(password)

def check_сase_complication(password):
    return any(ch.isupper() for ch in password) and any(ch.islower() for ch in password)

def check_digits(password):
    return any(ch.isdigit() for ch in password)

def check_special_characters(password):
    pattern = re.compile(r'[$*#!^%_?]')
    return re.findall(pattern,password)

def check_email(password):
    return re.search(r'[\w\.-]+@[\w\.-]+',password)

def check_phone_number(password):
    return re.search(r'[\dA-Z]{3}-[\dA-Z]{2}-[\dA-Z]{2}',password) or re.search(r'[\dA-Z]{3}-[\dA-Z]{7}',password)


def get_password_strength(password,file_path):
    strength = 10
    message = []


    if check_blacklist(file_path,password):
        strength -= 2
        message.append('Пароль не должен быть простым словом')

    if check_password_length(password) < 6:
        strength -= 1
        message.append('Длина пароля должна быть больше 6 символов')

    if not check_сase_complication(password):
        strength -= 1
        message.append('Пароль должен содержать символы в верхнем и нижнем регистрах')

    if not check_digits(password):
        strength -= 1
        message.append('Пароль должен содержать хотя бы одну цифру')

    if not check_special_characters(password):
        strength -= 1
        message.append('Пароль должен содержать специальные символы (#,!,^)')

    if check_email(password):
        strength -= 1
        message.append('Пароль не должен содержать email')

    if check_phone_number(password):
        strength -= 1
        message.append('Пароль не должен содержать номера телефонов')

    if strength < 1:
        strength = 1

    return strength,message


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--password", help="password for checking")
    parser.add_argument("-b", "--blacklist", help="file with blacklisted passwords")
    args = parser.parse_args()
    strength,message = get_password_strength(args.password,args.blacklist)
    print('Сложность пароля равна - ', strength)
    print('Что нужно исправить : ')
    for msg in message:
        print('-', msg)



