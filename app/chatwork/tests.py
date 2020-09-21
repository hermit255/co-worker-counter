from django.test import TestCase
from chatwork.models import Account
from datetime import date
from dateutil.relativedelta import relativedelta
from chatwork.views import get_diff


class ChatworkTestCase(TestCase):
  def setUp(self):
    # create 5 data of each month
    dates = list((date.today() - relativedelta(months=i)).isoformat() for i in range(3))
    for d in dates:
      for i in range(1, 5):
        Account.objects.create(account_id=i, name='user', department='department', date=d)

  def testMain(self):
    # delete 1 data of each date
    date_1 = (date.today() - relativedelta(months=0)).isoformat()
    date_2 = (date.today() - relativedelta(months=1)).isoformat()
    date_3 = (date.today() - relativedelta(months=2)).isoformat()
    Account.objects.filter(date=date_1, account_id=4).delete()
    Account.objects.filter(date=date_2, account_id=3).delete()
    Account.objects.filter(date=date_3, account_id=2).delete()
    actual_1 = get_diff(date_2, date_1)
    actual_2 = get_diff(date_3, date_2)
    self.assertEqual(3, actual_1['added'][0].account_id)
    self.assertEqual(4, actual_1['dropped'][0].account_id)
    self.assertEqual(2, actual_2['added'][0].account_id)
    self.assertEqual(3, actual_2['dropped'][0].account_id)