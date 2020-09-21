from django.db import models
from django.utils import timezone

class Account(models.Model):
    account_id = models.IntegerField()
    name = models.CharField(max_length=255, blank=True)
    department = models.CharField(max_length=255, blank=True)
    date = models.DateField(default=timezone.now)
    exception_flg = models.BooleanField(null=True)

    class Meta:
        unique_together = (("account_id","date"),)
