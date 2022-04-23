#!/usr/bin/env bash
cd "$(dirname "$0")"

xfce4-terminal -e '/root/tg_bot/run_scraper.sh' &

while true
do
	# python3 tg_bot.py | tee -a ../logs/bot.log
	python3 tg_bot.py
	bash crash_sender.sh
	sleep 2
done
