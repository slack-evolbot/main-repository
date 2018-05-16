# -*- coding: utf-8 -*-
from slackbot.bot import respond_to, listen_to
import re
from requests.exceptions import RequestException
import json
import time
import lirc
import random
import sys
sys.path.append("../")
import disp_test01
import os
sys.path.append("../chatSystem/")
import chat
import re

class TEMP_DATA():
    context_info = 'DUMMY'
    mode_info = 'dialog'

@listen_to(u'(おはようございます|しりとりしよう|.*？)')
@respond_to(u'(おはようございます|しりとりしよう|.*？)')
def resp_aplha(message, *something):
    lirc.init("test05", blocking = False)
    chat_message, TEMP_DATA.context_info, TEMP_DATA.mode_info = chat.main(message.body['text'], None, None)
    print(message.body['text'])   
    message.send(chat_message)

@listen_to(u'(^(?!(おはようございます|しりとりしよう|.*？)).+$)')
@respond_to(u'(^(?!(おはようございます|しりとりしよう|.*？)).+$)')
def resp_beta(message, *something):
    lirc.init("test05", blocking = False)
    chat_message, TEMP_DATA.context_info, TEMP_DATA.mode_info = chat.main(message.body['text'], TEMP_DATA.context_info, TEMP_DATA.mode_info)
    print(message.body['text'])
    message.send(chat_message)

    
