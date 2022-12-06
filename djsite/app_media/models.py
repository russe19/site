from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
import datetime

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.IntegerField(verbose_name=_('Balance'), default=0)
    status = models.ForeignKey('Status', on_delete=models.CASCADE, verbose_name=_('Status'))

    class Meta:
        verbose_name_plural = _('profiles')
        verbose_name = _('profile')


class Cover(models.Model):
    user = models.ForeignKey(User, verbose_name=_('User'), default=None, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name=_('Cover name'), blank=True, null=True)
    description = models.TextField(max_length=1000, verbose_name=_('Description'))
    created_at = models.DateField(verbose_name=_('Date create'), auto_now_add=True)
    price = models.IntegerField(verbose_name=_('Price'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('covers')
        verbose_name = _('cover')

class CoverImage(models.Model):
    entry = models.OneToOneField(Cover, verbose_name=_('Cover'), on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

    class Meta:
        verbose_name_plural = _('cover images')
        verbose_name = _('cover image')


class MusicText(models.Model):
    user = models.ForeignKey(User, verbose_name=_('User'), default=None, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name=_('Text name'), blank=True, null=True)
    description = models.TextField(max_length=1000, verbose_name=_('Description'))
    created_at = models.DateField(verbose_name=_('Date create'), auto_now_add=True)
    price = models.IntegerField(verbose_name=_('Price'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('music texts')
        verbose_name = _('music text')


class Music(models.Model):
    user = models.ForeignKey(User, verbose_name=_('User'), default=None, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name=_('Music name'), blank=True, null=True)
    description = models.TextField(max_length=1000, verbose_name=_('Description'))
    created_at = models.DateField(verbose_name=_('Date create'), auto_now_add=True)
    price = models.IntegerField(verbose_name=_('Price'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('musics')
        verbose_name = _('music')


class MusicSound(models.Model):
    entry = models.OneToOneField(Cover, verbose_name=_('Cover'), on_delete=models.CASCADE)
    image = models.ImageField(upload_to='musics/')

    class Meta:
        verbose_name_plural = _('music sounds')
        verbose_name = _('music sound')


class Status(models.Model):
    name = models.CharField(verbose_name=_('Status'), max_length=100)