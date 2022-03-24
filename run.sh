#!/usr/bin/env bash

cd "$(dirname "$0")"

while true
do
	python3 tg_bot.py | tee -a ../logs/bot.log
    bash crash_sender.sh
	sleep 2
done
