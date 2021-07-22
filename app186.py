import telebot
from config186 import keys, TOKEN
from extensions186 import ChangeException, Change

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def help(message: telebot.types.Message):
    text = 'Привет! Я могу:\nПоказать список доступных валют: /values\nСконвертировать валюты по команде:\n' \
'<имя валюты> <в какую валюту перевести> <количество переводимой валюты>\nНапомнить, что я могу: /help'
    bot.reply_to(message, text)
    
@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Я могу:\nПоказать список доступных валют: /values\nСконвертировать валюты по команде:\n' \
'<имя валюты> <в какую валюту перевести> <количество переводимой валюты>\nНапомнить, что я могу: /help'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ChangeException('Слишком много параметров')
        quote, base, amount = values
        total_base = Change.get_price(base, quote, amount)
    except ChangeException as e:
        bot.reply_to(message, f'Ваша ошибка:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Переводим {quote}. в {base}.\n{amount} {quote}. = {total_base} {base}.'
        bot.send_message(message.chat.id, text)

bot.polling()
