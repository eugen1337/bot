from telegram.ext import (Application, MessageHandler,
                          filters, ConversationHandler, CommandHandler)
from tokens import TG_TOKEN
from deep_translator import GoogleTranslator

from bs4 import BeautifulSoup

from markups import markup_start, markup_signs, markup_lng, markup_times
from fetches import fetch_phrase, fetch_compatibility, fetch_horoscope


async def ask_phrase_lng(update, context):
    await update.message.reply_text('Выберите язык', reply_markup=markup_lng)
    return 1


async def phrase(update, context):
    lang = update.message.text[:2]
    text = (await fetch_phrase())['daily']
    translated = GoogleTranslator(source='en', target=lang).translate(text)
    await update.message.reply_text(translated, reply_markup=markup_start)
    return ConversationHandler.END


async def start(update, context):
    text = 'Hello'
    await update.message.reply_text(text, reply_markup=markup_start)


async def start_compatibility(update, context):
    text = 'Choose first sign'
    await update.message.reply_text(text, reply_markup=markup_signs)

    return 1


async def first_sign(update, context):
    context.user_data['first sign'] = update.message.text.split(' —')[0]
    text = 'Choose second sign'
    await update.message.reply_text(text, reply_markup=markup_signs)

    return 2


async def second_sign(update, context):
    context.user_data['second sign'] = update.message.text.split(' —')[0]
    await update.message.reply_text('Result:\n', reply_markup=markup_start)
    await get_compatibility(update=update, context=context)

    return ConversationHandler.END


async def stop(update, context):
    text = 'OK'
    await update.message.reply_text(text, reply_markup=markup_start)

    return ConversationHandler.END


async def get_compatibility(update, context):
    text = ''

    for i in await fetch_compatibility(context=context):
        text += i['text']

    translated = GoogleTranslator(source='en', target='ru').translate(text)

    await update.message.reply_text(translated)


async def start_horo(update, context):
    text = 'Choose sign you want to know'
    await update.message.reply_text(text, reply_markup=markup_signs)

    return 1


async def get_sign(update, context):
    context.user_data['sign'] = update.message.text.split(' —')[0]
    text = 'Choose time'
    await update.message.reply_text(text, reply_markup=markup_times)

    return 2


async def get_time(update, context):
    context.user_data['time'] = update.message.text
    await update.message.reply_text(
        f"{context.user_data['sign']} horoscope for {context.user_data['time']}:\n",
        reply_markup=markup_start
    )
    await get_horoscope(update=update, context=context)

    return ConversationHandler.END


async def get_horoscope(update, context):
    page = await fetch_horoscope(context=context)

    soup = BeautifulSoup(page, "html.parser")
    HTML_cls = 'article__item article__item_alignment_left article__item_html'
    horo = soup.find('div', class_=HTML_cls)

    print(horo.text)

    await update.message.reply_text(horo.text)


def main():
    application = Application.builder().token(TG_TOKEN).build()

    application.add_handler(CommandHandler('start', start))

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
