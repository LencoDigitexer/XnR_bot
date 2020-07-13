print("Starting XnR_bot!")
import vk_api.vk_api
from vk_api.bot_longpoll import VkBotEventType
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
import sys, os, random
import asyncio, kb_gen
print("Libraries is OK")
# WARNING! if you start bot on heroku isLocal must be false
isLocal = False
# WARNING!

# for choice local cfg or cfg
if isLocal:
    from config_local import vk_api_token, vk_group_id, vk_prefix1, vk_prefix2, button_text, message1, message2, message3, Debug, delay_send, start_button_text
    print("Local config selected!")
else:
    from config import vk_api_token, vk_group_id, vk_prefix1, vk_prefix2, button_text, message1, message2, message3, Debug, delay_send, start_button_text
    print("Env config selected!")

class BotCore:
    def __init__(self, api_token, group_id, server_name: str = "Empty"):
        self.server_name = server_name
        self.vk = vk_api.VkApi(token=api_token)
        self.long_poll = VkBotLongPoll(self.vk, group_id)
        self.vk_api = self.vk.get_api()
        print("BotCore class initilaized!")

    #func for send message with keyboard
    async def send_msg_kb(self, send_id, message, kb):
        self.vk_api.messages.send(peer_id=send_id, message=message, keyboard=kb, random_id=get_random_id())
        return 1

    def adjust_message_text(self, msg):
        message_text = msg.encode()
        if len(message_text) < 4096:
            message_text = message_text * int(4096 / len(message_text))
            return message_text.decode()

    #func for spam
    async def spam(self, send_id, msg1, msg2, msg3, delay_send, button_txt):
        print("Starting raid conversation!")
        while True:
            try:
                kbs_s = kb_gen.gen(button_text)
                await self.send_msg_kb(send_id, random.choice([msg1, msg2, msg3]), kbs_s)
                await self.send_msg_kb(send_id, random.choice([msg1, msg2, msg3]), kbs_s)
                await self.send_msg_kb(send_id, random.choice([msg1, msg2, msg3]), kbs_s)
                await asyncio.sleep(delay_send)
            except vk_api.exceptions.ApiError as f:
                f2 = str(f)
                if f2 == "[9] Flood control: too much messages sent to user":
                    print("Flood control detected!")
                else:
                    print(f'Stopping raid this conversation. reason:{f}')
                    break

    #main cycle
    def start(self):
        print("XnR_bot started!")
        print("Starting listeing long poll!")
        for event in self.long_poll.listen():
                if Debug:
                    print(event)
                if event.type == VkBotEventType.MESSAGE_NEW:
                    last_id = event.object.peer_id
                    print("New message received from "+str(last_id))
                    # make button for activation raid
                    if event.object.text == '' or event.object.text == vk_prefix1+' rqb' or event.object.text == vk_prefix2+' rqb':
                        if event.object.text == '':
                            print("Joined to conversation!")
                            print("Sending keyboard")
                        else:
                            print("Request to send keyboard received!")
                            print("Sending keyboard")
                        kb = VkKeyboard(one_time=True)
                        kb.add_button(start_button_text, VkKeyboardColor.NEGATIVE)
                        kb_main = kb.get_keyboard()
                        ioloop = asyncio.get_event_loop()
                        wait_tasks = asyncio.wait([self.send_msg_kb(last_id, 'XnR_bot. Powered by Heroku. https://github.com/arturyudin/XnR_bot', kb_main)])
                        ioloop.run_until_complete(wait_tasks)
                        print("Keyboard sent!")
                    # starts raid to the conversation
                    if event.object.text == vk_prefix2+' '+start_button_text or event.object.text == vk_prefix1+' '+ start_button_text:
                        print("Message received for start raid!")
                        ioloop = asyncio.get_event_loop()
                        wait_tasks = asyncio.wait([self.spam(last_id, self.adjust_message_text(message1), self.adjust_message_text(message2)
                        , self.adjust_message_text(message3), delay_send, button_text)])
                        ioloop.run_until_complete(wait_tasks)
                        #self.send_msg_kb(last_id, 'Павук лох!', kb_main)


xnrBot = BotCore(vk_api_token, vk_group_id, "XnR_bot")
while True:
    xnrBot.start()
