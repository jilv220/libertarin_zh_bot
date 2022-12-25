#!/bin/bash
[ "$UID" -eq 0 ] || exec sudo bash "$0" "$@"

rm *.csv

pkg_name=${PWD##*/} 
cp -r ./ /opt/${pkg_name}
chmod a+w /opt/${pkg_name}/twitter_bot.db

cp twitter-bot.service.example twitter-bot.service
sed -i "s/PWD/${pkg_name}/g" twitter-bot.service
cp twitter-bot.service /etc/systemd/system/twitter-bot.service
cp twitter-bot.timer.example /etc/systemd/system/twitter-bot.timer

rm twitter-bot.service