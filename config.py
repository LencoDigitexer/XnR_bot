# config for raid bot with env (for heroku and v1.0)
import os

vk_api_token = os.environ.get('vk_api_tokenn')
vk_group_id = os.environ.get('vk_group_id')
vk_prefix1 = os.environ.get('vk_prefix1')
vk_prefix2 = os.environ.get('vk_prefix2')
button_text = os.environ.get('button_text')
message1 = os.environ.get('message1')
message2 = os.environ.get('message2')
message3 = os.environ.get('message3')
start_button_text = os.environ.get('start_button_text')

#don't touch this
Debug = False
delay_send = 0.1
