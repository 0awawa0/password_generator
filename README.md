# password_generator

Программа предназначена для генерации безопасных паролей. Программа запоминает все выданные ей пароли в виде хешей в текстовом файле (т.н. базе данных), благодаря чему программа не выдает одинаковые пароли.

Аргументы для работы с программой:

* -l/--length LENGTH - длина генерируемого пароля, по-умолчанию 16
* -nr/--NoRussian - флаг, отключает использование кирилицы
* -np/--NoPunctuation - флаг, отключает исользование пунктуации
* -s/--show - флаг, если установлен, сгенерированный пароль отобразится на экране
* -ns/--NoSave - флаг, если установлен, хеш сгенерированного пароля не сохранится в базе данных
* -c/--count - задает количество генерируемых паролей, по-умолчанию равное единице. Если передано значение большее единице,
все генерируемые пароли выводятся на экран и не копируются в буфер обмена.
* -p/--phrase PHRASE - генерация пароля на основе переданной фразы, в этом режиме игнорируются -l, -ns, -nr и -c. Длина пароля
зависит только от переданной фразы, пароль не сохраняется в базе данных, не содержит русских символов. Также не гарантируется безопасность пароля.

Примеры работы программы:
```bash
> genpass
Пароль скопирован в буфер обмена
```

```bash
> genpass -l 10 -s
W:эa/Ё@НЩэ
Пароль скопирован в буфер обмена
```

```bash
> genpass -l 10 -s -np -nr
j3Aj71Sgux
Пароль скопирован в буфер обмена
```

```bash
> genpass -s --phrase "Векторная сумма импульсов всех тел системы есть величина постоянная, если векторная сумма внешних сил, дейтсвующих на систему тел, равна нулю."
V$!V7$3Vp3v$V$dN$7rN
Пароль скопирован в буфер обмена
```