import psycopg2
INTENTS = [
    {
        'name': 'Дата проведения',
        'token': ('когда', 'сколько', 'дата', 'дату'),
        'scenario': None,
        'answer': 'Выпускной балл проводится 7ого марта, и начнется в 18:00.'
    },
    {
        'name': 'Место проведения',
        'token': ('где', 'место', 'локация', 'адрес', 'метро'),
        'scenario': None,
        'answer': 'Выпускной балл проводится в отеле Гранд.'
    },
    {
        'name': 'Регистрация',
        'token': ('регист', 'добав', 'записат', 'запиши'),
        'scenario': 'registration',
        'answer': None
    }
]

SCENARIOS = {
    'registration': {
        'first step': 'step1',
        'steps': {
            'step1': {
                'text': 'Чтобы зарегистрироваться, введите ваше имя. Оно будет написано на бэйдже.',
                'failure_text': 'Имя должно состоять из 2-30 букв и дефиса. Попробуйте еще раз.',
                'handler': 'handler_name',
                'next_step': 'step2'
            },
            'step2': {
                'text': 'Введите email. Мы отправим на него все данные.',
                'failure_text': 'Во введенном адресе ошибка. Попробуйте еще раз.',
                'handler': 'handler_email',
                'next_step': 'step3'
            },
            'step3': {
                'text': 'Спасибо за регистрацию, {name}! Мы отправили на {email} билет, копию мы отправили во вложении.',
                'image': 'generate_ticket_handler',
                'failure_text': None,
                'handler': None,
                'next_step': None
            }
        }
    }
}
DEFAULT_ANSWER = 'Не знаю как на это ответить.' \
                 'Могу сказать, когда и где пройдет выпускной балл, а также зарегистрировать вас. Просто спросите.'

DB_CONFIG = dict(
    provider='postgres',
    user='postgres',
    host='localhost',
    password='B10vvyMz',
    database='vk_chat_bot',
    options='-c client_encoding=utf8'
)