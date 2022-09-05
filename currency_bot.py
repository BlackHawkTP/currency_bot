import telebot
import requests

Token = "5713195228:AAFtk7uIbPgeJBqLk0p-O1z3GR91i62OaY0"
bot = telebot.TeleBot(Token)

currencies = {
    'доллар': 'USD',
    'рубль': 'RUB',
    'евро': 'EUR',
}


class ConversionException(Exception):
    pass


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Добро пожаловать, {message.chat.username}!\n"
                                      f"Этот бот поможет вам узнать курс валют на данный момент!\n"
                                      f"Чтобы работать с данным ботом, укажите сначала сумму перевода, а затем имя валюты и в какую валюту перевести.\n"
                                      f"Например: 100 рубль доллар\n"
                                      f"/start - перезапустить бота, /values - валюты, /help - помощь")


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, f"Чтобы работать с данным ботом, укажите сначала сумму перевода, а затем имя валюты и в какую валюту перевести.\n"
                                      f"Например: 100 рубль доллар")


@bot.message_handler(commands=['values'])
def send_values(message):
    text = "Доступные валюты:"
    for currency in currencies.keys():
        text = '\n'.join((text, currency))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message):
    payload = {}
    headers = {
        "apikey": "KXHLjM5dVx2tSbqVu6LoAKmhkbQOJJL1"
    }

    values = message.text.split(' ')
    amount, fr, to = values

    if len(values) > 3:
        raise ConversionException("Слишком много параметров.")
    if to == fr:
        raise ConversionException(f"Невозможно перевести одинаковые валюты: {fr}")
    try:
        to_ticker = currencies[to]
    except KeyError:
        raise ConversionException(f"Не удалось обработать валюту {to}")
    try:
        fr_ticker = currencies[fr]
    except KeyError:
        raise ConversionException(f"Не удалось обработать валюту {fr}")
    try:
        amount = float(amount)
    except ValueError:
        raise ConversionException(f"Не удалось обработать количество {amount}")

    url = f"https://api.apilayer.com/fixer/convert?to={to_ticker}&from={fr_ticker}&amount={amount}"
    response = requests.request("GET", url, headers=headers, data=payload)
    result = response.text
    bot.send_message(message.chat.id, result)


bot.polling()
