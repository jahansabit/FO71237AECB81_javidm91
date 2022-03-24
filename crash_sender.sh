#!/usr/bin/env bash

TELEGRAM_BOT_TOKEN="5229280387:AAE4SFcTLiDuspR01GydekNgjiLpSSF5qdY"

curl -X POST \
     -H 'Content-Type: application/json' \
     -d '{"chat_id": "-744965364", "text": "Bot was crashed just now. Please check the logs on the server via VNC.", "disable_notification": false}' \
     https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage