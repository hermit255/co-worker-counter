#!bin/sh
echo "ROOM_ID=$ROOM_ID" >> /etc/environment
echo -e "\n" >> /etc/environment
echo "CHATWORK_API_TOKEN=$CHATWORK_API_TOKEN" >> /etc/environment
echo -e "\n" >> /etc/environment
crontab /script/crontab
cron -f