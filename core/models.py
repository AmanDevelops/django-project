from django.db import models


class UserData(models.Model):
    telegram_username = models.CharField(max_length=50)
