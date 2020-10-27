# Group settings
api_token = "496091a930976a73a6fc3555773179ff582d62958eea8ce10c34abf675ca349d2887d5749bcf89d9628eb"
group_id = 193797788

# Settings for lessons.py
db_addr = "37.140.192.23"
db_user = "u1054344_9g"
db_password = "N3u2J2z8"
db_name = "u1054344_9g"
weekday_translator = {1:'mon', 2:'tue', 3:'wed', 4:'thu', 5:'fri', 6:'sat', 7:'sun'}

import os

# Bot settings
debug = True
admins = eval(os.environ.get('admins'))
access = eval(os.environ.get('access'))
isClosed = int(os.environ.get('isClosed'))

version = "0.3"
watermark = "\nv"+version+"\nЕсли есть не точность, пишите в группу\nhttps://arturyudin.site/itsme"
