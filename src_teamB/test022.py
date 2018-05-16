import requests, json

WEB_HOOK_URL = "https://hooks.slack.com/services/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"

while True:
    request_data = requests.get(WEB_HOOK_URL)
    print(request_data.text)
