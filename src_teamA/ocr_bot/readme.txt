Slackでアップロードされた画像を文字に起こすbot。
画像から文字への変換は、MicrosoftのAPIを利用。
以下手順を参考に作成可能。
・手順書「・17_顔認識システム.xlsx」の[１．Face API Keyの取得]を実施済みである必要がある。

以下の値を変更の上起動すること。
slackbot_settings.py
・API_TOKEN（Slackbotのトークン）
・KEY1（Microsoft Vision APIのキー）
