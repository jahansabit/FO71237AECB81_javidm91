#!/usr/bin/env bash

while true
do
	python3 tg_bot.py
    bash crash_sender.sh
	sleep 2
done
