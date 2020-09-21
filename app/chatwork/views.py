from django.shortcuts import render
from django.http import HttpResponse
from chatwork.models import Account
import requests
from datetime import date
from dateutil.relativedelta import relativedelta
from django.db.models import Count
import environ
env = environ.Env(DEBUG=(bool, False))

# Create your views here.

def show(request):
    diff_list = list()
    for i in range(6):
        end = (date.today() - relativedelta(months=i)).isoformat()
        start = (date.today() - relativedelta(months=(i+1))).isoformat()
        diff_list.append(get_diff(start, end))

    params = dict(d1=diff_list[0], d2=diff_list[1], d3=diff_list[2], d4=diff_list[3], d5=diff_list[4], d6=diff_list[5])
    return render(request, 'chatwork/show.html', params)

def get_diff(start, end):
    query = Account.objects.filter(date__gte=start, date__lte=end).values('date').annotate(Count('date'))
    if len(query) < 2:
        return dict(period='no comparable data found during ' + start + ' ~ ' + end, added=list(), dropped=list())
    latest = query.order_by('-date')[0]['date'].isoformat()
    oldest = query.order_by('date')[0]['date'].isoformat()
    period = oldest + '~' + latest

    data_latest = Account.objects.filter(date=latest) or list()
    if end == date.today().isoformat() and not data_latest:
        base = 'https://api.chatwork.com/v2/'
        end_point = 'contacts'
        api_token = env('CHATWORK_API_TOKEN')
        headers = {'X-ChatWorkToken': api_token, 'Content-Type': 'application/x-www-form-urlencoded'}
        res = requests.get(base + end_point, headers=headers)
        for contact in res.json():
            data = dict(account_id=contact['account_id'], name=contact['name'][:2], department=contact['department'], date=date.today().isoformat())
            Account.objects.update_or_create(**data)
        data_today = Account.objects.filter(date=latest)
    data_oldest = Account.objects.filter(date=oldest) or list()

    ids_latest = data_latest.values_list('account_id', flat=True) if data_latest else list()
    ids_oldest = data_oldest.values_list('account_id', flat=True) if data_oldest else list()

    added = Account.objects.filter(date=latest).filter(account_id__in=ids_latest).exclude(account_id__in=ids_oldest)
    dropped = Account.objects.filter(date=oldest).filter(account_id__in=ids_oldest).exclude(account_id__in=ids_latest)

    return dict(period=period, added=added, dropped=dropped)
