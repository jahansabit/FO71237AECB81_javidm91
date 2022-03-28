#!/usr/bin/env bash
cd "$(dirname "$0")"

while true
do
	xfce4-terminal -e 'python3 scraper_bot.py' &
	python3 tg_bot.py | tee -a ../logs/bot.log
	bash crash_sender.sh
	sleep 2
done
