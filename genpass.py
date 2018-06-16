import random
import string
import hashlib
import pyperclip
import argparse


russian_letters = "АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя"


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
    args = parser.parse_args()

    # Запусаем главный цикл программы
    main(args)

