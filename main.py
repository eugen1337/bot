from telegram.ext import (Application, MessageHandler,
                          filters, ConversationHandler, CommandHandler)
from tokens import TG_TOKEN, PATH

from markups import markup_start, markup_signs, markup_lng, markup_times
from model import get_compatibility, get_horoscope, get_phrase, get_joke


async def joke(update, context):
    text = (await get_joke(context=context))[0]
    await update.message.reply_text(text, reply_markup=markup_start)

    log(update, update.message.text, text)


async def ask_phrase_lng(update, context):
    text = 'Выберите язык'
    await update.message.reply_text(text, reply_markup=markup_lng)

    log(update, update.message.text, text)

    return 1


async def phrase(update, context):
    context.user_data['lang'] = update.message.text
    text = await get_phrase(context)
    await update.message.reply_text(text, reply_markup=markup_start)

    log(update, update.message.text, text)

    return ConversationHandler.END


async def start(update, context):
    text = 'Здравствуйте, я бот по астрологии'
    await update.message.reply_text(text, reply_markup=markup_start)

    log(update, update.message.text, text)


async def stop(update, context):
    text = 'OK'
    await update.message.reply_text(text, reply_markup=markup_start)

    log(update, update.message.text, text)

    return ConversationHandler.END


async def start_compatibility(update, context):
    text = 'Выберите первый знак зодиака'
    await update.message.reply_text(text, reply_markup=markup_signs)

    log(update, update.message.text, text)

    return 1


async def first_sign(update, context):
    context.user_data['first sign'] = update.message.text.split(' —')[0]
    text = 'Выберите второй знак зодиака'
    await update.message.reply_text(text, reply_markup=markup_signs)

    log(update, update.message.text, text)

    return 2


async def second_sign(update, context):
    context.user_data['second sign'] = update.message.text.split(' —')[0]

    text = 'Совместимость {} и {}:\n'.format(
        context.user_data['first sign'],
        context.user_data['second sign']
    ) + await get_compatibility(context=context)

    await update.message.reply_text(text, reply_markup=markup_start)

    log(update, update.message.text, text)

    return ConversationHandler.END


async def start_horo(update, context):
    text = 'Выберите знак зодиака'
    await update.message.reply_text(text, reply_markup=markup_signs)

    log(update, update.message.text, text)

    return 1


async def get_sign(update, context):
    context.user_data['sign'] = update.message.text.split(' —')[0]
    text = 'Выберите период'
    await update.message.reply_text(text, reply_markup=markup_times)

    log(update, update.message.text, text)

    return 2


async def get_time(update, context):
    context.user_data['time'] = update.message.text

    text = 'Гороскоп для {} за период - {}:\n'.format(
        context.user_data['sign'],
        context.user_data['time']
    ) + await get_horoscope(context=context)

    await update.message.reply_text(text, reply_markup=markup_start)

    log(update, update.message.text, text)

    return ConversationHandler.END


def log(update, user_text, bot_text):
    with open(PATH + str(update.message.from_user.id) + '.log',
              'a',
              encoding='utf-8') as file:
        file.write('User: ' + user_text + '\n')
        file.write('Bot: ' + bot_text + '\n\n')


def main():
    application = Application.builder().token(TG_TOKEN).build()

    application.add_handler(CommandHandler('start', start))

    application.add_handler(CommandHandler('Joke', joke))

    conv_handler_signs = ConversationHandler(
        entry_points=[CommandHandler('Compatibility', start_compatibility)],

        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_sign)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_sign)],
        },

        fallbacks=[CommandHandler('exit', stop)]
    )
    application.add_handler(conv_handler_signs)

    conv_handler_phrase = ConversationHandler(
        entry_points=[CommandHandler('Phrase', ask_phrase_lng)],

        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, phrase)],
        },

        fallbacks=[CommandHandler('exit', stop)]
    )
    application.add_handler(conv_handler_phrase)

    conv_handler_horo = ConversationHandler(
        entry_points=[CommandHandler('Horoscope', start_horo)],

        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_sign)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_time)],
        },

        fallbacks=[CommandHandler('exit', stop)]
    )
    application.add_handler(conv_handler_horo)

    application.run_polling()


if __name__ == '__main__':
    main()
