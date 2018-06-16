import random
import string
import hashlib
import pyperclip
import argparse


russian_letters = "АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя"

translit = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d",
    "е": "e", "ё": "e", "ж": "j", "з": "z", "и": "i",
    "й": "i", "к": "k", "л": "l", "м": "m", "н": "n",
    "о": "o", "п": "p", "р": "r", "с": "s", "т": "t",
    "у": "u", "ф": "f", "х": "h", "ц": "c", "ч": "c",
    "ш": "s", "щ": "s", "э": "e", "ю": "u", "я": "y"
}

numbers = {
    "a": "4",
    "b": "8",
    "e": "3",
    "g": "9",
    "i": "1",
    "o": "0",
    "s": "5",
    "t": "7"
}

punct = {
    "a": "@",
    "i": "!",
    "s": "$"
}


# Генерация пароля
def generate(symbols, args):

    # Начальное значение - пустая строка, хэш - None,  и значение флагов False
    result = ""
    pas_hash = None

    # Флаги нужны для проверки безопасности пароля
    flags = {"has_digits": False,
             "has_punctuation": False,
             "has_upper": False,
             "has_lower": False,
             "has_rus": False
             }

    # Проверка аргументов командной строки
    if not args.nopunct:
        flags["has_punctuation"] = True
    if not args.norus:
        flags["has_rus"] = True

    # check хранит результат проверки наличия пароля в базе данных, если True - пароля нет
    check = False

    # Генерация пароля
    while (False in flags.values()) and not check:
        for i in range(args.length):

            # Берем случайный символ из переднного массива
            char = random.choice(symbols)

            # Проверяем что это за символ и устанавливаем соответствующий флаг
            if char in string.digits:
                flags["has_digits"] = True
            if char in string.ascii_lowercase:
                flags["has_lower"] = True
            if char in string.ascii_uppercase:
                flags["has_upper"] = True
            if char in string.punctuation:
                flags["has_punctuation"] = True
            if char in russian_letters:
                flags["has_rus"] = True

            # Добавляем символ к результирующему паролю
            result += char

        # Берем хеш от пароля и проверяем его по базе данных
        pas_hash = hashlib.sha512()
        pas_hash.update(result.encode())
        check = check_database(pas_hash)

    # Сгенерированный пароль записываем в базу данных и возвращаем результат функции
    if not args.nosave:
        with open("database.db", 'a') as f:
            f.write(pas_hash.hexdigest() + '\n')
    return result


# Генерация пароля из фразы
def gen_from_phrase(args):
    phrase = args.phrase
    phrase = str.lower(phrase).split(" ")
    result = ""

    # Получем первые буквы слов в фразе
    for word in phrase:
        result += word[0]

    # Переводим буквы в транслит
    for k in translit.keys():
        result = result.replace(k, translit[k])

    # Переводим некоторые буквы в спец. символы и цифры
    for k in result:
        if args.nopunct:
            if k in punct.keys():
                result = result.replace(k, punct[k])
            elif k in numbers.keys():
                result = result.replace(k, numbers[k])
        else:
            if k in numbers.keys():
                result = result.replace(k, numbers[k])

    # Переводим буквы в верхний регистр случайным образом
    result = list(result)
    for k in range(len(result)):
        coin = random.getrandbits(1)
        if coin:
            result[k] = result[k].upper()
    result = "".join(result)

    # Возвращаем результат
    return result


# Проверка базы данных на наличие хеша
def check_database(hash):
    try:
        with open("database.db", 'r') as f:
            db = f.readlines()
        if hash in db:
            return False
        else:
            return True
    except FileNotFoundError:
            return True


# Главнаая функция
def main(args):

    if args.phrase:
        password = gen_from_phrase(args)
    else:
        # Формируем список символов
        symbols = string.ascii_letters + string.digits
        symbols += russian_letters if args.norus else ""
        symbols += string.punctuation if args.nopunct else ""

        # Генерируем пароль
        password = generate(symbols, args)

    # Возвращаем результат
    if args.show:
        print(password)
    pyperclip.copy(password)
    print("Пароль скопирован в буфер обмена")


if __name__ == "__main__":
    # Парсим аргументы командной строки
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--length", default=16, type=int)
    parser.add_argument("-nr", "--NoRussian", action="store_false", dest="norus")
    parser.add_argument("-np", "--NoPunctuation", action="store_false", dest="nopunct")
    parser.add_argument("-s", "--show", action="store_true", dest="show")
    parser.add_argument("-ns", "--NoSave", action="store_true", dest="nosave")
    parser.add_argument("-p", "--phrase", type=str, dest="phrase", default=None)
    args = parser.parse_args()

    # Запусаем главный цикл программы
    main(args)

