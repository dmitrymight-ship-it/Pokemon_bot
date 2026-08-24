import telebot
from config import TOKEN
from random import randint
from logic import Pokemon, Wizard, Fighter
from telebot import types

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['go'])
def start(message):
    if message.from_user.username not in Pokemon.pokemons.keys():
        chance = randint(1, 3)
        if chance == 1:
            pokemon = Pokemon(message.from_user.username)
        elif chance == 2:
            pokemon = Wizard(message.from_user.username)
        elif chance == 3:
            pokemon = Fighter(message.from_user.username)
        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, pokemon.show_img())
    else:
        bot.reply_to(message, "Ты уже создал себе покемона")


@bot.message_handler(commands=['attack'])
def attack_pok(message):
    if message.reply_to_message:
        if message.reply_to_message.from_user.username in Pokemon.pokemons.keys() and message.from_user.username in Pokemon.pokemons.keys():
            enemy = Pokemon.pokemons[message.reply_to_message.from_user.username]
            pok = Pokemon.pokemons[message.from_user.username]
            res = pok.attack(enemy)
            bot.send_message(message.chat.id, res)
        else:
            bot.send_message(message.chat.id, "Сражаться можно только с покемонами")
    else:
        bot.send_message(message.chat.id, "Чтобы атаковать, нужно ответить на сообщения того, кого хочешь атаковать")


@bot.message_handler(commands=['info'])
def info_(message):
    bot.reply_to(message, """\
Я универсальный телеграмм бот:
С моей помощью вы можете создать себе покемона используя функцию /go
Также вы можете его покормить используя функцию /variant, а с функцией /attack ты сможешь начать бой с покемоном.
Удачи!\
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
