from deep_translator import GoogleTranslator

from bs4 import BeautifulSoup

from fetches import (fetch_phrase,
                     fetch_compatibility,
                     fetch_horoscope,
                     fetch_joke)


async def get_horoscope(context):
    time = context.user_data['time']
    translated = GoogleTranslator(source='ru', target='en').translate(time)
    context.user_data['time'] = translated.lower()

    page = await fetch_horoscope(context=context)

    soup = BeautifulSoup(page, "html.parser")
    HTML_cls = 'article__item article__item_alignment_left article__item_html'
    horo = soup.find('div', class_=HTML_cls)

    return horo.text


async def get_joke(context):
    resp = await fetch_joke()

    text = GoogleTranslator(source='en', target='ru').translate(resp['value'])
    img = resp['icon_url']

    return [text, img]


async def get_compatibility(context):
    resp = await fetch_compatibility(context=context)
    text = ''

    for i in resp:
        text += i['text']

    translated = GoogleTranslator(source='en', target='ru').translate(text)

    return translated


async def get_phrase(context):
    lang = context.user_data['lang']
    target = GoogleTranslator(source='ru', target='en').translate(lang).lower()

    text = (await fetch_phrase())['daily']

    translated = GoogleTranslator(
         source='en',
         target=target[:2]
    ).translate(text)

    return translated
