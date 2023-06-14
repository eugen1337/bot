from telegram import ReplyKeyboardMarkup

keyboard_start = [
    ['/Compatibility', '/Phrase', '/Horoscope', '/Joke']
]

keyboard_languages = [
    ['Русский', 'Английский', 'Французский', 'Немецкий']
]

keyboard_times = [
    ['Сегодня', 'Завтра', 'Неделя', 'Месяц', 'Год']
]

keyboard_signs = [
    ['Aries — Овен', 'Taurus — Телец', 'Gemini — Близнецы'],
    ['Cancer — Рак', 'Leo — Лев', 'Virgo — Дева'],
    ['Libra — Весы', 'Scorpio — Скорпион', 'Sagittarius — Стрелец'],
    ['Capricorn — Козерог', 'Aquarius — Водолей ', 'Pisces — Рыбы']
]

markup_start = ReplyKeyboardMarkup(keyboard_start, one_time_keyboard=False,
                                   resize_keyboard=True)

markup_signs = ReplyKeyboardMarkup(keyboard_signs, one_time_keyboard=False,
                                   resize_keyboard=True)

markup_lng = ReplyKeyboardMarkup(keyboard_languages, one_time_keyboard=False,
                                 resize_keyboard=True)

markup_times = ReplyKeyboardMarkup(keyboard_times, one_time_keyboard=False,
                                   resize_keyboard=True)
