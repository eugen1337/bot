from tokens import RAPID_KEY
import aiohttp


async def fetch_phrase():
    url = "https://horoscope-astrology.p.rapidapi.com/dailyphrase"

    headers = {
        "X-RapidAPI-Key": RAPID_KEY,
        "X-RapidAPI-Host": "horoscope-astrology.p.rapidapi.com"
    }

    return await get_response(url=url, headers=headers, params={})


async def fetch_compatibility(context):
    url = "https://horoscope-astrology.p.rapidapi.com/affinity"

    params = {"sign1": context.user_data['first sign'],
              "sign2": context.user_data['second sign']}

    headers = {
        "X-RapidAPI-Key": RAPID_KEY,
        "X-RapidAPI-Host": "horoscope-astrology.p.rapidapi.com"
    }

    return await get_response(url, headers, params)


async def fetch_joke():
    u = "https://matchilling-chuck-norris-jokes-v1.p.rapidapi.com/jokes/random"

    headers = {
        "accept": "application/json",
        "X-RapidAPI-Key": "1ae4315f08mshf21ff730e37ac66p1e7327jsnd25b38193dc5",
        "X-RapidAPI-Host": "matchilling-chuck-norris-jokes-v1.p.rapidapi.com"
    }

    return await get_response(url=u, headers=headers, params={})


async def fetch_horoscope(context):
    # https://horo.mail.ru/prediction/libra/tomorrow/

    url = ('https://horo.mail.ru/prediction/' +
           context.user_data['sign'].lower() + '/' +
           context.user_data['time'].lower())

    return await get_response(url, headers={}, params={}, type='html')


async def get_response(url, headers, params, type='json'):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url=url, params=params) as resp:
            if type == 'html':
                return await resp.text()
            else:
                return await resp.json()
