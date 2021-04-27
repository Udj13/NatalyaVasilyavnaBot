# NatalyaVasilyavnaBot
## Описание
Этот простой бот нужен для регулярной проверки новых платежей на организацию в интерфейсе от разработчиков ООО «БСС».
Принцип работы: открываем одну организацию, проверяем все платежи. Если платежа еще нет в базе, то кидаем его в чатик и добавляем в базу.
Если описание содержит ключевое слово, то дублируем в альтернитивный чатик.

Ключевой момент - всё запускается и работает на VDS, без графического интерфейса.

## Используемые технологии

Парсинг - selenium

Виртуальный дисплей - xvfb

База данных - sqlite3

## Подготовка сервера

Традиционно обновляемся:

**apt-get update**

**apt-get upgrade**

Устанавливаем виртуальный дисплей:
**apt-get install xvfb**

Устанавливаем браузер:
**apt-get install chromium-browser**

Смотрим версию:
**chromium-browser --version**

Качаем нужный web driver для selenium:
https://chromedriver.chromium.org/downloads


Например, результат проверки версии:

Chromium 89.0.4389.90 Built on Ubuntu , running on Ubuntu 16.04

Качаем тут:

https://chromedriver.storage.googleapis.com/index.html?path=89.0.4389.23/

## Установка скрипта

**python3 -m venv /myenv/NatalyaVasilevna**

**cd /myenv/NatalyaVasilevna**

Активируем окружение:

**. /bin/activate**

Устанавливаем модули Пайтон:

**pip install --upgrade pip**

**pip3 install pyTelegramBotAPI**

**pip3 install xvfbwrapper**

**pip3 install selenium**

Создаем файл conf.py:

```python
usr = "логин"
pwd = "пароль"
key_api = 'ключ бота'
chat_id = 'основной чат'
filter_tag = 'ключевое_слово_для_фильтра'
altrnative_chat_id = 'альтеративный чат '
total_chat_id = ''
path_to_driver = '/home/chromedriver'
path_to_site = 'сайт клиент-банка'
```

**chmod -x main.py**

Проверка того что скрипт запускается (но без базы выдаст ошибку):

**python3 main.py**

Выходим из виртуального окружения:

**deactivate**

## Создание базы

Созаем базу данных в любом внешнем редакторе, например SQLiteStudio.

Формат таблиц в базе данных (индивидуальная для каждой организации):

```sql
CREATE TABLE Transactions (
    [key]             INT    PRIMARY KEY,
    pp_num            STRING,
    pp_name_of_client STRING,
    pp_inn            STRING,
    pp_summ           STRING,
    pp_info           STRING
);
```

## Ставим таймер на регулярный запуск

Копируем файлы .service и .timer в /etc/systemd/system/

Обновляем сервисы:

**systemctl daemon-reload**

Проверка запуска сервиса (должен корректно отработать):

**systemctl start natalyavasilyavna.service**

Статус последнего запуска:

**systemctl status natalyavasilyavna.service**

Запуск таймера для проверки:

**systemctl start natalyavasilyavna.timer**

Включить таймер:

**systemctl enable natalyavasilyavna.timer**

Статус таймера:

**systemctl status natalyavasilyavna.timer**

Настройки таймера:
```
OnCalendar=*-*-* *:15:*
OnCalendar=*-*-* *:45:*
```
означают что он запускается в 15 и 45 минут каждого часа (в итоге получается два раза в час с интервалом 30 минут).
