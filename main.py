import aiohttp
from telegram.ext import (Application, MessageHandler,
                          filters, ConversationHandler, CommandHandler)
from telegram import ReplyKeyboardMarkup
from tokens import TG_TOKEN, RAPID_KEY
from deep_translator import GoogleTranslator

keyboard_start = [
    ['/Compatibility', '/Phrase']
]

keyboard_languages = [
    ['russian', 'english', 'france', 'deutsch', 'exit']
]

keyboard_signs = [
    ['Aries — Овен', 'Taurus — Телец', 'Gemini — Близнецы'],
    ['Cancer — Рак', 'Leo — Лев', 'Virgo — Дева'],
    ['Libra — Весы', 'Scorpio — Скорпион', 'Sagittarius — Стрелец'],
    ['Capricorn — Козерог', 'Aquarius — Водолей ', 'Pisces — Рыбы']
]

markup_start = ReplyKeyboardMarkup(keyboard_start, one_time_keyboard=False)
markup_signs = ReplyKeyboardMarkup(keyboard_signs, one_time_keyboard=False)
markup_lng = ReplyKeyboardMarkup(keyboard_languages, one_time_keyboard=False)


async def ask_phrase_lng(update, context):
    await update.message.reply_text('Выберите язык', reply_markup=markup_lng)
    return 1


async def phrase(update, context):
    lang = update.message.text[:2]
    text = (await fetch_phrase())['daily']
    translated = GoogleTranslator(source='en', target=lang).translate(text)
    await update.message.reply_text(translated, reply_markup=markup_start)
    return ConversationHandler.END


async def fetch_phrase():
    url = "https://horoscope-astrology.p.rapidapi.com/dailyphrase"

    headers = {
        "X-RapidAPI-Key": RAPID_KEY,
        "X-RapidAPI-Host": "horoscope-astrology.p.rapidapi.com"
    }

    params = {}

    json_resp = await get_response(url=url, headers=headers, params=params)

    return json_resp


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
    url = "https://horoscope-astrology.p.rapidapi.com/affinity"

    params = {"sign1": context.user_data['first sign'],
              "sign2": context.user_data['second sign']}

    headers = {
        "X-RapidAPI-Key": RAPID_KEY,
        "X-RapidAPI-Host": "horoscope-astrology.p.rapidapi.com"
    }

    json_resp = await get_response(url, headers, params)

    # if not response['response']['GeoObjectCollection']['featureMember']:
    #     await update.message.reply_text('No such objects founded')
    #     return

    text = ''

    for i in json_resp:
        text += i['text']

    translated = GoogleTranslator(source='en', target='ru').translate(text)

    await update.message.reply_text(translated)


async def get_response(url, headers, params):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url=url, params=params) as resp:
            return await resp.json()


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

    application.run_polling()


if __name__ == '__main__':
    main()
