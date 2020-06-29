import googletrans
from googletrans import Translator
import requests
import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
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


def translate(text, src="ru", dest="uk"):
    result = translator.translate(text, src=src, dest=dest)
    return result.text

def send_msg(msg):
    vk.messages.send(
        user_id=event.user_id,
        random_id=event.random_id,
        message=msg
    )


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


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        send_msg(translate(event.text))


print(translate("перевод на украинский язык"))
