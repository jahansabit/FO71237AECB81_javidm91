#!/usr/bin/env bash
cd "$(dirname "$0")"

while true
do
	# python3 scraper_bot.py | tee -a ../logs/bot.log
	python3 scraper_bot.py
	bash crash_sender.sh
	sleep 2
done
