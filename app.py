import telebot
import requests
import json
from config import TOKEN
from extensions import APIException, Convertor
import traceback

bot = telebot.TeleBot(TOKEN)

keys = {
    "рубль": 'RUB',
    "доллар": 'USD',
    "евро": 'EUR'}

@bot.message_handler(commands=['start', 'help'])
def help(massage: telebot.types.Message):
    text = 'Для начала работы введите команду боту в следующем формате:<имя валюты, цену которой хотите узнать> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>. ' \
           '\nСписок доступных валют вызывается командой: /values'
    bot.reply_to(massage, text)

@bot.message_handler(commands=['values'])
def values(massage: telebot.types.Message):
    text = 'Доступные к обмену валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(massage, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров!')

        answer = Convertor.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)

@bot.message_handler(content_types=['text'])
def convert(massage: telebot.types.Message):
    base, quote, amount = massage.text.split()
    #http://api.exchangeratesapi.io/v1/latest?access_key=f023799a91c0951703fea661271f073a&base={keys[quote]}&symbols={keys[base]}
    r = requests.get(f'http://api.exchangeratesapi.io/v1/latest?access_key=f023799a91c0951703fea661271f073a&base={keys[quote]}&symbols={keys[base]}')
    total_base = json.loads(r.content)
    total_base = total_base['rates'][keys[base]] * int(amount)
    total_base = round(total_base, 2)
    text = f'Цена {amount} {quote} в {base} - {total_base}'
    bot.send_message(massage.chat.id, text)




bot.polling(none_stop=True)
