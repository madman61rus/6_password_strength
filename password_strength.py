import argparse
import os
import re

def check_blacklist(file_path, password):
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r', encoding='utf-8') as data_file:
        blacklisted_keys = data_file.read().split()
        data_file.close()
        if password in blacklisted_keys:
            return 2,'Пароль не должен быть простым словом'
        else:
            return 0,None

def check_password_length(password,length=6):
    if len(password) < length :
        return 1 , 'Длина пароля должна быть больше 6 символов'
    else :
        return 0,None

def check_сase_complication(password):
    if not any(ch.isupper() for ch in password) and any(ch.islower() for ch in password):
        return 1, 'Пароль должен содержать символы в верхнем и нижнем регистрах'
    else:
        return 0,None

def check_digits(password):
    if not any(ch.isdigit() for ch in password):
        return 1, 'Пароль должен содержать хотя бы одну цифру'
    else:
        return 0,None

def check_regular_expression(password,pattern,message):
    if re.search(pattern,password):
        return 1, message
    else:
        return 0, None



def get_password_strength(password,file_path,strength=10):

    message = []


    functions = [check_blacklist(file_path,password),check_password_length(password),check_сase_complication(password),
                 check_regular_expression(password,r'[^$*#!^%_?]',
                                          'Пароль должен содержать специальные символы (#,!,^)'),
                 check_regular_expression(password, r'[\w\.-]+@[\w\.-]+','Пароль не должен содержать email'),
                 check_regular_expression(password, r'[\dA-Z]{3}-[\dA-Z]{2}-[\dA-Z]{2}',
                                          'Пароль не должен содержать номера телефонов'),
                 check_regular_expression(password, r'[\dA-Z]{3}-[\dA-Z]{7}',
                                          'Пароль не должен содержать номера телефонов')
                 ]

    for function in functions:
        check_result = function
        strength -= check_result[0]
        if check_result[0]:
            message.append(check_result[1])



    return strength, message


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



