import vk_api.vk_api
from vk_api.bot_longpoll import VkBotEventType
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

import config
import Lessons, logicHandler


class BotCore:
    def __init__(self, api_token, group_id):
        self.vk = vk_api.VkApi(token=api_token)
        self.long_poll = VkBotLongPoll(self.vk, group_id)
        self.vk_api = self.vk.get_api()

    def get_user_name(self, user_id):
        id = self.vk_api.users.get(user_id=user_id)[0]["first_name"]
        return id
    def send_msg(self, user_id, message):
        self.vk_api.messages.send(peer_id=user_id, message=message, random_id=get_random_id())
    def send_msg_keyboard(self, user_id, message, keyboard):
        self.vk_api.messages.send(peer_id=user_id, message=message, random_id=get_random_id(), keyboard=keyboard)

    def makeDo(self, user_id, peer_id, username, text):
        # elif text == "!refresh":
        #     if user_id in config.admins:
        #         config.refreshConfig()
        #         kb = logicHandler.LogicHandler().mainMenuKeyboard()
        #         self.send_msg_keyboard(peer_id, "OK!", kb)
        #     else:
        #         self.send_msg(peer_id, "Pososi. Чтобы получить админ права пиши [id331320136|@st4ck3r].")

        if text == "На сегодня" or text == "[club193797788|@9g_bot] На сегодня":
            raw_lessons = Lessons.get_lessons()
            if raw_lessons == "no_data_for_day" or raw_lessons == "table_not_exists":
                text_lessons = "На сегодня уроков нет\n"
                kb = logicHandler.LogicHandler().mainMenuKeyboard()
                text_lessons += config.watermark
                self.send_msg_keyboard(peer_id, text_lessons, kb)
            else:
                text_lessons = "Расписание на сегодня\n"
                for i in raw_lessons:
                    text_lessons += str(str(i[0])+". "+i[4]+"-"+i[5]+" | "+i[1]+" (№"+i[2]+") "+" "+i[3]+"\n")
                kb = logicHandler.LogicHandler().mainMenuKeyboard()
                text_lessons += config.watermark
                self.send_msg_keyboard(peer_id, text_lessons, kb)

        elif text == "На завтра" or text == "[club193797788|@9g_bot] На завтра":
            raw_lessons = Lessons.get_lessons(1)
            if raw_lessons == "no_data_for_day" or raw_lessons == "table_not_exists":
                text_lessons = "На завтра уроков нет\n"
                kb = logicHandler.LogicHandler().mainMenuKeyboard()
                text_lessons += config.watermark
                self.send_msg_keyboard(peer_id, text_lessons, kb)
            else:
                text_lessons = "Расписание на завтра\n"
                for i in raw_lessons:
                    text_lessons += str(str(i[0])+". "+i[4]+"-"+i[5]+" | "+i[1]+" (№"+i[2]+") "+" "+i[3]+"\n")
                kb = logicHandler.LogicHandler().mainMenuKeyboard()
                text_lessons += config.watermark
                self.send_msg_keyboard(peer_id, text_lessons, kb)

        elif text == "На всю неделю" or text == "[club193797788|@9g_bot] На всю неделю":
            kb = logicHandler.LogicHandler().mainMenuKeyboard()
            self.send_msg_keyboard(peer_id, "In progress...", kb)

    def start(self):
        for event in self.long_poll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                user_id = event.object.message['from_id']
                peer_id = event.object.message['peer_id']
                username = self.get_user_name(user_id)
                text = event.object.message['text']
                print("Get New Message! Username: "+username+", Text: '"+text+"', Type: ", end="")
                if event.object.message['id'] > 0:
                    print("private message")
                    isPrivateMessage = True
                    isChatMessage = False
                else:
                    print("chat message")
                    isPrivateMessage = False
                    isChatMessage = True
                
                if config.debug:
                    print(event)
                if text == "Start" or text == "Начать":
                    kb = logicHandler.LogicHandler().mainMenuKeyboard()
                    self.send_msg_keyboard(peer_id, "Hello ебать!", kb)

                elif text == "!deploy":
                    if user_id in config.admins:
                        kb = logicHandler.LogicHandler().mainMenuKeyboard()
                        self.send_msg_keyboard(peer_id, "Кнопки бота отправлены", kb)
                    else:
                        self.send_msg(peer_id, "Pososi. Чтобы получить админ права пиши [id331320136|@st4ck3r].")
                
                elif text == "!undeploy":
                    if user_id in config.admins:
                        kb = logicHandler.LogicHandler().emptyKeyboard()
                        self.send_msg_keyboard(peer_id, "Кнопки бота удалены", kb)
                    else:
                        self.send_msg(peer_id, "Pososi. Чтобы получить админ права пиши [id331320136|@st4ck3r].")
                else:
                    if config.isClosed:
                        if user_id in config.access:
                            self.makeDo(user_id, peer_id, username, text)
                        else:
                            kb = logicHandler.LogicHandler().mainMenuKeyboard()
                            self.send_msg_keyboard(peer_id, "Бот в приватном режиме. Для использования требуется подписка 10р/неделя.\n За подробностями писать в группу.", kb)
                    else:
                        self.makeDo(user_id, peer_id, username, text)

server1 = BotCore(config.api_token, config.group_id)
server1.start()
