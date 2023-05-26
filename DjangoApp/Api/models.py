from django.db import models


class Transaction(models.Model):
    payer = models.CharField(max_length=100)
    points = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
