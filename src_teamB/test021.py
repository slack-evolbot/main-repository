import requests, json

WEB_HOOK_URL = "https://hooks.slack.com/services/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"
requests.post(WEB_HOOK_URL, data = json.dumps({
    'text': u'HELLO.',
    'username': u'WEB_HOOK_BOT',
    'icon_emoji': u':smile_cat:',
    'link_names': 1,
}))
