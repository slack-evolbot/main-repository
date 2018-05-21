Slackでアップロードされた画像を文字に起こすbot。
画像から文字への変換は、MicrosoftのAPIを利用。
以下手順を参考に作成可能。
・p7_RaspberryPi3_SlackBot.ods
・RaspberryPi_顔認識&勤怠管理.xlsx[２．Face API Keyの取得]

以下の値を変更の上起動すること。
slackbot_settings.py
・API_TOKEN（Slackbotのトークン）
・KEY1（Microsoft Vision APIのキー）
