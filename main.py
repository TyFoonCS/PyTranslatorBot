import googletrans
from googletrans import Translator
import requests
import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

languages_dict = googletrans.LANGUAGES
translator = Translator()


class MyVkLongPoll(VkLongPoll):
    def listen(self):
        while True:
            try:
                for event in self.check():
                    yield event
            except Exception as e:
                print('error vk', e)


def translate(text, dest="uk"):
    result = translator.translate(text, dest=dest)
    return result.text


def send_msg(msg, photo=None):
    try:
        if not photo:
            if event.from_chat:
                vk.messages.send(
                    chat_id=event.chat_id,
                    random_id=event.random_id,
                    keyboard=keyboard.get_keyboard(),
                    message=msg
                )
            else:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=event.random_id,
                    keyboard=keyboard.get_keyboard(),
                    message=msg
                )
        else:
            if event.from_chat:
                vk.messages.send(
                    chat_id=event.chat_id,
                    random_id=event.random_id,
                    keyboard=keyboard.get_keyboard(),
                    message=msg,
                    attachment=photo
                )
            else:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=event.random_id,
                    keyboard=keyboard.get_keyboard(),
                    message=msg,
                    attachment=photo
                )
    except BaseException:
        pass


session = requests.Session()

# Авторизация пользователя:
"""
login, password = 'python@vk.com', 'mypassword'
vk_session = vk_api.VkApi(login, password)
try:
    vk_session.auth(token_only=True)
except vk_api.AuthError as error_msg:
    print(error_msg)
    return
"""

# Авторизация группы
# vk_session = vk_api.VkApi(token='cdee8de69235cd55519d36971817b3c5cd46b641660d8e8b99841ebff6c920e4f477549032655319203e6')

vk_session = vk_api.VkApi(token='cdee8de69235cd55519d36971817b3c5cd46b641660d8e8b99841ebff6c920e4f477549032655319203e6')

vk = vk_session.get_api()

upload = VkUpload(vk_session)  # Для загрузки изображений
longpoll = MyVkLongPoll(vk_session)

keyboard = VkKeyboard(one_time=True)

keyboard.add_button('#помощь#', color=VkKeyboardColor.DEFAULT)

bot_words_dict = {
    "#помощь#": """
    Список команд:\n
    #папа# - мой создатель №1,\n
    #мама# - мой создатель №2
    """,
    "#пасхалка#": "Дима лох",
}

bot_photo_dict = {
    "#папа#": "photo167849130_457241934",
    "#мама#": "photo182293940_457242552"
}

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        words = event.text.lower().split()

        if words[0] in bot_words_dict.keys():
            send_msg(bot_words_dict[words[0]])
        elif words[0] in bot_photo_dict.keys():
            send_msg(words[0], bot_photo_dict[words[0]])
        else:
            send_msg(translate(event.text))
