from django.core.management.base import BaseCommand

from chatwork.models import Account
from chatwork.views import get_diff

from datetime import date
from dateutil.relativedelta import relativedelta
import environ
import requests
env = environ.Env(DEBUG=(bool, False))

class Command(BaseCommand):
    def handle(self, *args, **options):
        today = date.today().isoformat()
        #yesterday = (date.today() - relativedelta(days=1)).isoformat()
        yesterday = (date.today() - relativedelta(months=1)).isoformat()
        data = get_diff(yesterday, today)
        report_title = data['period']
        report_added = 'added: ' + '(' + str(len(data['added'])) + ')' + ' / '.join(list(d.name for d in data['added']))
        report_dropped = 'dropped: ' + '(' + str(len(data['dropped'])) + ')' + ' / '.join(list(d.name for d in data['dropped']))
        report = """
{report_title}
{report_added}
{report_dropped}
        """.format(report_title=report_title, report_added=report_added, report_dropped=report_dropped).strip()

        base = 'https://api.chatwork.com/v2/'
        room_id = env('ROOM_ID')
        end_point = 'rooms/' + room_id + '/messages'
        api_token = env('CHATWORK_API_TOKEN')
        headers = {'X-ChatWorkToken': api_token, 'Content-Type': 'application/x-www-form-urlencoded'}
        payload = dict(body=report, self_unread=1)
        res = requests.post(base + end_point, headers=headers, params=payload)