# -*- coding: utf-8 -*-
from slackbot.bot import respond_to, listen_to
import re
from requests.exceptions import RequestException

@listen_to(u'(おはようございます)')
@respond_to(u'(おはようございます)')
def resp_aplha(message, *something):
    message.send(u'おはよー')
