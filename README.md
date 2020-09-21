# co-worker-counter
## how to use
1. Copy .env.example as .env.
2. Replace the value of environment variables to your chatwork-api-token and room_id.
    - about chatwork-api-token: https://developer.chatwork.com/ja/
3. Type command `docker-compose up` in your terminal
    - requires command `docker-comopse`
    - At first time, application image will be build automatically.
4. Access `http://localhost:8888` with your borwser, then you can see report.
    - You can see monthly difference of contact members.

## collect data
1. Exec `sh /script/export_environment.sh` to enable cron
    - Cron get contact list on AM6:00 every day
    - Cron send report to your chatwork room(defined by environment variables ROOM_ID).
    - Report tell you difference between todays contact member and tommorow's one.