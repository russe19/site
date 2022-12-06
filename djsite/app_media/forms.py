from django import forms
from django.contrib.auth.forms import UserCreationForm
from app_media.models import Profile, MusicText, Music, Cover
from django.utils.translation import gettext_lazy as _

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text=_('First name'))
    last_name = forms.CharField(max_length=30, required=False, help_text=_('Last name'))
    email = forms.EmailField(required=False, help_text=_('Email'))
    balance = forms.IntegerField(help_text=_('Balance'), min_value=0, max_value=99999999999)


class RegisterFormUpdate(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('balance',)


class CoverForm(forms.Form):
    name = forms.CharField(max_length=50, help_text=_('Cover name'))
    description = forms.CharField(widget=forms.Textarea, max_length=1000, help_text=_('Description'))
    images = forms.ImageField(help_text=_('Files'))
    price = forms.IntegerField(help_text=_('Price'), min_value=0, max_value=999999)


class MusicForm(forms.Form):
    name = forms.CharField(max_length=50, help_text=_('Music name'))
    description = forms.CharField(widget=forms.Textarea, max_length=1000, help_text=_('Description'))
    files = forms.FileField(help_text=_('Audio'))
    price = forms.IntegerField(help_text=_('Price'), min_value=0, max_value=999999)


class TextForm(forms.Form):
    name = forms.CharField(max_length=50, help_text=_('Text name'))
    description = forms.CharField(widget=forms.Textarea, max_length=1000, help_text=_('Description'))
    price = forms.IntegerField(help_text=_('Price'), min_value=0, max_value=999999)


class BalanceForm(forms.Form):
    count = forms.IntegerField(help_text=_('Up balance'), min_value=0, max_value=9999999)


class HistoryForm(forms.Form):
    day = forms.IntegerField(help_text=_('The period for which we request the history'),
                              min_value=0, max_value=365, required=False)