from telegram import ReplyKeyboardMarkup

keyboard_start = [
    ['/Compatibility', '/Phrase', '/Horoscope']
]

keyboard_languages = [
    ['russian', 'english', 'france', 'deutsch', 'exit']
]

keyboard_times = [
    ['today', 'tomorrow', 'week', 'month', 'year']
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
markup_times = ReplyKeyboardMarkup(keyboard_times, one_time_keyboard=False)
