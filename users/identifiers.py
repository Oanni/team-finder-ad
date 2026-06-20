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
COLOR_RED = '#FF0000'
COLOR_GREEN = '#00FF00'
COLOR_BLUE = '#0000FF'
COLOR_ORANGE = '#FFA500'
COLOR_PURPLE = '#800080'
COLOR_DARK_BLUE = '#00008B'
COLOR_PINK = '#FFC0CB'

PORTRAIT_PALETTE = [
    COLOR_RED,
    COLOR_GREEN,
    COLOR_BLUE,
    COLOR_ORANGE,
    COLOR_PURPLE,
    COLOR_DARK_BLUE,
    COLOR_PINK,
]
PORTRAIT_EDGE = 200
PORTRAIT_GLYPH_SIZE = 120
PORTRAIT_HASH_DIGEST_SIZE = 4
PORTRAIT_FALLBACK_MAILBOX = 'user'
PORTRAIT_TYPEFACE = (
    "static/fonts/"
    "Neue_Haas_Grotesk_Display_Pro_75_Bold.otf"
)

ABOUT_TEXTAREA_ROWS = 4
GITHUB_HOST = 'github.com'

MEMBER_PAGE_SIZE = 12
