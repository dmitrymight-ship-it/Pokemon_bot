import telebot
from config import TOKEN
from logic import Pokemon
from telebot import types

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['go'])
def go(message):
    if message.from_user.username not in Pokemon.pokemons.keys():
        pokemon = Pokemon(message.from_user.username)
        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, pokemon.show_img())
    else:
        bot.reply_to(message, "Ты уже создал себе покемона")



@bot.message_handler(commands=['help'])
def info_(message):
    bot.reply_to(message, """\
Я универсальный телеграмм бот:
С моей помощью вы можете создать себе покемона используя функцию /go
Также вы можете его покормить используя функцию /variant\
""")


@bot.message_handler(commands=["variant"])
def send_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    corm1 = types.KeyboardButton("Сухой корм")
    corm2 = types.KeyboardButton("Влажный корм")
    corm3 = types.KeyboardButton("Стекловата")
    markup.add(corm1, corm2, corm3)

    bot.send_message(
        message.chat.id,
        "Выберите вариант:",
        reply_markup=markup
    )


@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text == "Сухой корм":
        bot.reply_to(message, "Вы накормили своего покемона: сухим кормом")
    elif message.text == "Влажный корм":
        bot.reply_to(message, "Вы накормили своего покемона: влажным кормом")
    elif message.text == "Стекловата":
        bot.reply_to(message, "Вы накормили своего покемона: стекловатой")
    else:
        bot.reply_to(message, "Пожалуйста, выберите вариант из кнопок.")


bot.infinity_polling(none_stop=True)

