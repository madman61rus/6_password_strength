import argparse
import os
import re

def check_blacklist(file_path, password):
    '''Проверка на присутствие пароля в черном списке'''
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r', encoding='utf-8') as data_file:
        blacklisted_keys = data_file.read().split()
        data_file.close()
        if password in blacklisted_keys:
            return 2,'Пароль не должен быть простым словом'
        else:
            return 0,None

def check_password_length(password):
    '''Проверка длины пароля'''
    if len(password) < 6 :
        return 1 , 'Длина пароля должна быть больше 6 символов'
    else :
        return 0,None

def check_сase_complication(password):
    '''Проверка на содержание больших и маленьких букв'''
    if not any(ch.isupper() for ch in password) and any(ch.islower() for ch in password):
        return 1, 'Пароль должен содержать символы в верхнем и нижнем регистрах'
    else:
        return 0,None

def check_digits(password):
    '''Проверка на присутсвие цифр в пароле'''
    if not any(ch.isdigit() for ch in password):
        return 1, 'Пароль должен содержать хотя бы одну цифру'
    else:
        return 0,None

def check_special_characters(password):
    '''Проверка на присутствие специальных символов'''
    pattern = re.compile(r'[$*#!^%_?]')
    if not re.findall(pattern,password):
        return 1, 'Пароль должен содержать специальные символы (#,!,^)'
    else:
        return 0,None

def check_email(password):
    '''Проверка на присутствие email в пароле'''
    if re.search(r'[\w\.-]+@[\w\.-]+',password):
        return 1,'Пароль не должен содержать email'
    else:
        return 0,None

def check_phone_number(password):
    '''Проверка на присутствие номеров телефонов в пароле'''
    if re.search(r'[\dA-Z]{3}-[\dA-Z]{2}-[\dA-Z]{2}',password) or re.search(r'[\dA-Z]{3}-[\dA-Z]{7}',password):
        return 1, 'Пароль не должен содержать номера телефонов'
    else:
        return 0,None


def get_password_strength(password,file_path):
    '''Функция вычисления сложности'''

    strength = 10
    message = []

    tmp = check_blacklist(file_path,password)
    strength -= tmp[0]
    message.append(tmp[1])

    functions = [check_password_length,check_сase_complication,check_digits,check_special_characters ,check_email,check_phone_number,check_phone_number]

    for func in functions:
        tmp = func(password)
        strength -= tmp[0]
        if tmp[1]:
            message.append(tmp[1])

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



