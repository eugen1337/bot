from deep_translator import GoogleTranslator

from bs4 import BeautifulSoup

from fetches import fetch_phrase, fetch_compatibility, fetch_horoscope


async def get_horoscope(context):
    page = await fetch_horoscope(context=context)

    soup = BeautifulSoup(page, "html.parser")
    HTML_cls = 'article__item article__item_alignment_left article__item_html'
    horo = soup.find('div', class_=HTML_cls)

    return horo.text


async def get_compatibility(context):
    resp = await fetch_compatibility(context=context)
    text = ''

    for i in resp:
        text += i['text']

    translated = GoogleTranslator(source='en', target='ru').translate(text)

    return translated


async def get_phrase(context):
    lang = context.user_data['lang']
    text = (await fetch_phrase())['daily']
    translated = GoogleTranslator(source='en', target=lang).translate(text)

    return translated
