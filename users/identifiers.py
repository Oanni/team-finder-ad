# Ограничения полей модели User (имена полей не меняются)
NAME_MAX_LENGTH = 124
SURNAME_MAX_LENGTH = 124
PHONE_MAX_LENGTH = 12
ABOUT_MAX_LENGTH = 256
SECRET_MIN_LEN = 8

# Нормализация телефона
LOCAL_DIGIT_COUNT = 10
COUNTRY_DIGIT_COUNT = 11
LEGACY_PREFIX = '8'
UNIFIED_PREFIX = '7'

# Ключи фильтра каталога участников
FAVORITE_OWNERS_KEY = 'owners-of-favorite-projects'
JOINED_VENTURE_OWNERS_KEY = 'owners-of-participating-projects'
ADMIRERS_OF_MINE_KEY = 'interested-in-my-projects'
MY_VENTURE_MEMBERS_KEY = 'participants-of-my-projects'

CATALOG_FILTER_LABELS = {
    FAVORITE_OWNERS_KEY: 'Авторы избранных проектов',
    JOINED_VENTURE_OWNERS_KEY: 'Авторы проектов, в которых я участвую',
    ADMIRERS_OF_MINE_KEY: 'Пользователи, которым нравятся мои проекты',
    MY_VENTURE_MEMBERS_KEY: 'Участники моих проектов',
}

# Генерация портрета
PORTRAIT_PALETTE = [
    '#FF0000',
    '#00FF00',
    '#0000FF',
    '#FFA500',
    '#800080',
    '#00008B',
    '#FFC0CB',
]
PORTRAIT_EDGE = 200
PORTRAIT_GLYPH_SIZE = 120
PORTRAIT_TYPEFACE = (
    "static/fonts/"
    "Neue_Haas_Grotesk_Display_Pro_75_Bold.otf"
)

MEMBER_PAGE_SIZE = 12
