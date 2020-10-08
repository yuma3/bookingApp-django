from django.db import models
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _#国際化
from django.core.mail import send_mail
from django.utils import timezone


"""Booking Model"""


class Store(models.Model):
    """store model"""
    name = models.CharField('店舗', max_length=255)
    # address = models.CharField('住所', max_length=255)
    # phone_num = models.IntegerField('電話番号')
    # email = models.EmailField('メールアドレス')

    def __str__(self):
        return self.name


class Staff(models.Model):
    """店舗スタッフ"""
    """User model はUserよりSettings Auth＿user＿modelを使うのがベター"""
    name = models.CharField('表示名', max_length=55)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='ログインユーザー', on_delete=models.CASCADE)
    store = models.ForeignKey(Store, verbose_name='店舗', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'store'], name='unique_staff'),
        ]

    def __str__(self):
        return f'{self.store.name} - {self.name}'


class Schedule(models.Model):
    """予約スケジュール"""

    start = models.DateTimeField('開始時間')
    end = models.DateTimeField('終了時間')
    name = models.CharField('予約者名', max_length=255)
    staff = models.ForeignKey(Staff, verbose_name='スタッフ', on_delete=models.CASCADE)

    def __str__(self):
        start = timezone.localtime(self.start).strftime('%Y-%m-%d %H:%M:%S')
        end = timezone.localtime(self.end).strftime('%Y-%m-%d %H:%M:%S')
        return f'{self.name} {start}~{end} {self.staff}'
