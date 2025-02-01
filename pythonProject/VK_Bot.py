import requests
import vk_api
from pony.orm import db_session
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import logging
import settings
import handlers
from Models import UserState, Registration


def config_log():
    log = logging.getLogger('Bot')
    stream_handler = logging.StreamHandler()
    file_handler = logging.FileHandler("bot.log", 'w', 'utf-8')

    stream_formater = logging.Formatter('%(levelname)s - %(message)s')
    file_formater = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%d %m %Y - %H:%M')

    stream_handler.setFormatter(stream_formater)
    file_handler.setFormatter(file_formater)

    log.addHandler(stream_handler)
    log.addHandler(file_handler)

    log.setLevel(logging.DEBUG)
    stream_handler.setLevel(logging.INFO)
    file_handler.setLevel(logging.DEBUG)

    return log


group_id = 227409188
log = config_log()


class Bot:
    """
    Use Python 3.12
    """

    def __init__(self, group_id, token):
        self.group_id = group_id
        self.token = token
        self.vk = vk_api.VkApi(token=token)
        self.poller = VkBotLongPoll(self.vk, self.group_id)
        self.api = self.vk.get_api()

    def run(self):
        for event in self.poller.listen():
            log.debug(f'получено событие {event.type}')
            try:
                self.on_event(event)
            except Exception:
                log.exception(f'ошибка')

    @db_session
    def on_event(self, event):
        if event.type != VkBotEventType.MESSAGE_NEW:
            log.info(f'я не умею обрабатывать {event.type}')
            return
        text = event.message['text']
        user_id = str(event.message['peer_id'])
        log.debug(f'пользователь с id {user_id} отпрвавил сообщение {text}')

        state = UserState.get(user_id=user_id)

        if state is not None:
            log.debug(f'пользователь продолжает регистрирование')
            self.continue_scenario(text=text, state=state, user_id=user_id)
        else:
            #search intent
            log.debug(f'ищем intent')
            for intent in settings.INTENTS:
                if any(token in text for token in intent['token']):
                    #run intent
                    if intent['answer']:
                        log.debug(f'найден intent')
                        self.send_text(intent['answer'], user_id)
                    else:
                        log.debug(f'пользователь начинает регистрацию')
                        self.start_scenario(intent['scenario'], user_id, text)
                    break
            else:
                log.debug(f'пользователь ввел неверное сообщение')
                self.send_text(settings.DEFAULT_ANSWER, user_id)

    def send_image(self, image, user_id):
        upload_url = self.api.photos.getMessagesUploadServer()['upload_url']
        upload_data = requests.post(url=upload_url, files={'photo': ('image.png', image, 'image/png')}).json()
        image_data = self.api.photos.saveMessagesPhoto(**upload_data)

        owner_id = image_data[0]['owner_id']
        media_id = image_data[0]['id']
        attachment_id = f'photo{owner_id}_{media_id}'

        self.api.messages.send(
            attachment=attachment_id,
            random_id=random.randint(1, 2 ** 20),
            peer_id=user_id
        )
        log.debug(f'отправлено фото')

    def send_step(self, step, user_id, text, context):
        if 'text' in step:
            self.send_text(step['text'].format(**context), user_id)
        if 'image' in step:
            handler = getattr(handlers, step['image'])
            image = handler(text, context)
            self.send_image(image, user_id)

    def send_text(self, text_to_send, user_id):
        self.api.messages.send(
            message=text_to_send,
            random_id=random.randint(1, 2 ** 20),
            peer_id=user_id
        )
        log.debug(f'отправлено сообщение {text_to_send}')

    def start_scenario(self, scenario_name, user_id, text):
        scenario = settings.SCENARIOS[scenario_name]
        first_step = scenario['first step']
        step = scenario['steps'][first_step]
        self.send_step(step, user_id, text, context={})
        UserState(user_id=user_id, scenario_name=scenario_name, step_name=first_step, context={})

    def continue_scenario(self, text, state, user_id):
        steps = settings.SCENARIOS[state.scenario_name]['steps']
        step = steps[state.step_name]

        handler = getattr(handlers, step['handler'])
        if handler(text=text, context=state.context):
            # next step
            next_step = step['next_step']
            self.send_step(steps[next_step], user_id, text, context=state.context)

            if steps[next_step]['next_step']:
                # switch to next step
                state.step_name = next_step
            else:
                log.debug(f'пользователь с именем {state.context['name']} завершил регистрацию ' \
                          f'и ввел почту {state.context['email']}')
                Registration(name=state.context['name'], email=state.context['email'])
                state.delete()
        else:
            text_to_send = step['failure_text']
            self.send_text(text_to_send, user_id)
            # retry step
