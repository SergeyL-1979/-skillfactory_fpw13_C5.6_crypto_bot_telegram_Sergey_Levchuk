import telebot
from config_bot import keys, TOKEN
from extensions import APIException, ConverterBot


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_command(message: telebot.types.Message):
    text = 'Привет! Я могу показать вам курсы обмена. \n '+' '\
'Для начала работы нажмите /help. '
    bot.reply_to(message, text)


@bot.message_handler(commands=['help'])
def help_command(message: telebot.types.Message):
    text = 'Чтобы начать работу дайте команду боту в следующем виде: \n'+''\
'<имя валюты> <имя валюты в которую надо перевести> <количество первой валюты> \n '+''\
'Между валютами один пробел и название валюты с маленькой буквы, например: "доллар рубль 1" \n '+''\
'Чтобы узнать курсы обмена, нажмите /values.\n '+' '\

    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        val_param = message.text.split(' ')

        if len(val_param) != 3:
            raise APIException('Слишком много или мало параметров \n /help')

        quote, base, amount = val_param
        total_base = ConverterBot.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)