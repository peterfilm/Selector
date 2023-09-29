import json
import re

def load_api_keys():
    '''
    Достаем файлы из настроек
    '''
    with open('config.json') as file:
        data = json.load(file)
        return data


def load_key_to_api(name, value):
    '''
    Изменяем данные в настройках config.json
    name - ключ
    value - значение
    '''
    data = load_api_keys()
    data[name] = value
    with open('config.json', "w") as file:
        json.dump(data, file, indent=2)


conf = load_api_keys()
name_of_file = re.compile(r"(?<!\S)(?<!\.)[а-яА-Яa-zA-ZёЁ\d\~@#$%\^\-_\(\)\{\}'`]{1,100}(?!\S)")
only_digits = re.compile(r"[\d]+")
