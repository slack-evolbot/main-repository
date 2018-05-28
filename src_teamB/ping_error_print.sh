#!/bin/bash
 
HOST=192.168.20.254
EROOR_COUNTER=0
NOW_ERROR=FALSE

while :
do
    ping -w 5 -n -c 1 $HOST >> /dev/null
    if [ $? -eq 0 ]
    then
      sleep 5
    else
	if [$ERROR_COUNTER > 3]
	then

	else
	    DT=`date "+%Y年%m月%d日%H時%M分%S秒"`
	    curl -X POST --data-urlencode 'payload={"channel": "[チャンネル名]", "username": "PINGさん", "text": "'$DT' ホスト['$HOST']が落ちたよ", "icon_emoji": ":[アイコン名]:"}' https://hooks.slack.com/services/xxxxxxxxxx/xxxxxxxxx/xxxxxxxxxxxxxxxxxxxxxx
	fi
    fi
done
