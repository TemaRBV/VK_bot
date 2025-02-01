from copy import copy
from unittest import TestCase
from unittest.mock import patch, Mock
from VK_Bot import Bot
import settings
from Token import token

class BotTests(TestCase):
    def test_run(self):
        INPUTS = [
            'Привет',
            'А что будет и когда',
            'Где будет',
            'Можешь зарегистрировать меня?',
            'Артем',
            'адрес artem-ryabov-1999@mail.ru',
            'artem-ryabov-1999@mail.ru'
        ]
        EXPECTED_OUTPUTS = [
            settings.DEFAULT_ANSWER,
            settings.INTENTS[0]['answer'],
            settings.INTENTS[1]['answer'],
            settings.SCENARIOS['registration']['steps']['step1']['text'],
            settings.SCENARIOS['registration']['steps']['step2']['text'],
            settings.SCENARIOS['registration']['steps']['step2']['failure_text'],
            settings.SCENARIOS['registration']['steps']['step3']['text'].format(name='Артем',
                                                                                email='artem-ryabov-1999@mail.ru')
        ]

        RAW_EVENT = [Mock() for i in range(len(INPUTS))]
        for mock, input in zip(RAW_EVENT, INPUTS):
            mock.type = 'message_new'
            mock.message = {'text': input, 'peer_id': 178054739}

        with patch('VkBotLongPoll.listen') as mock_poller:
            mock_poller.return_value = RAW_EVENT
        with patch('vk_api.VkApi(token=token).get_api().messages.send') as mock_sender:
            pass
        Bot.run()

