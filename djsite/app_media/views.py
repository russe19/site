from django.shortcuts import render, redirect, Http404
from django.contrib.auth.views import LoginView, LogoutView
from app_media.models import Profile, Cover, CoverImage, MusicText, Music, MusicSound, Status
from app_media.forms import RegisterForm, CoverForm, MusicForm, TextForm, RegisterFormUpdate
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import UpdateView, View, TemplateView, ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User, Group
from django.views.generic.edit import FormView
from django.utils.translation import gettext as _
import datetime
import logging

logger_login = logging.getLogger('login_logout')
logger_balance = logging.getLogger('balance')

def stat(balance, user):
    if balance >= 0 and balance < 1000:
        if Status.objects.filter(name='Новичек').exists():
            status = Status.objects.get(name='Новичек')
        else:
            status = Status.objects.create(name='Новичек')
        try:
            if not user.profile.status.name=='Новичек':
                logger_balance.info(f'Пользователь {user} перешел в статус "Новичек"')
        except ObjectDoesNotExist:
            logger_balance.info(f'Пользователь {user} перешел в статус "Новичек"')


    if balance >= 1000 and balance < 10000:
        if Status.objects.filter(name='Продвинутый').exists():
            status = Status.objects.get(name='Продвинутый')
        else:
            status = Status.objects.create(name='Продвинутый')
        try:
            if not user.profile.status.name=='Продвинутый':
                logger_balance.info(f'Пользователь {user} перешел в статус "Продвинутый"')
        except ObjectDoesNotExist:
            logger_balance.info(f'Пользователь {user} перешел в статус "Продвинутый"')

    if balance >= 10000:
        if Status.objects.filter(name='Эксперт').exists():
            status = Status.objects.get(name='Эксперт')
        else:
            status = Status.objects.create(name='Эксперт')
        try:
            if not user.profile.status.name=='Эксперт':
                logger_balance.info(f'Пользователь {user} перешел в статус "Эксперт"')
        except ObjectDoesNotExist:
            logger_balance.info(f'Пользователь {user} перешел в статус "Эксперт"')
    return status


class Login(LoginView):
    template_name = 'app_media/login.html'

class Logout(LogoutView):
    template_name = 'app_media/logout.html'
    next_page = 'entres'


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'app_media/register.html'
    success_url = '/main'

    def form_valid(self, form):
        user = form.save()
        user.first_name = form.cleaned_data.get('first_name')
        user.last_name = form.cleaned_data.get('last_name')
        user.email = form.cleaned_data.get('email')
        user.save()
        balance = form.cleaned_data.get('balance')
        status = stat(balance, user)
        Profile.objects.create(user=user, status=status, balance=balance)
        for image in self.request.FILES.getlist('images'):
            entry_image = CoverImage.objects.create(profile=user.profile, image=image)
            entry_image.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return redirect('/main')



class Update(UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'app_media/update.html'
    success_url = reverse_lazy('main')
    fields = ['first_name', 'last_name', 'email']


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = RegisterFormUpdate(instance=self.object.profile)
        return context

    def test_func(self):
        return self.request.user.id == self.kwargs['pk']

    def form_valid(self, form):
        profile_model = Profile.objects.get(user_id=self.object.id)
        profile_model.balance = self.request.POST['balance']
        profile_model.status = stat(profile_model.balance, self.request.user)
        profile_model.save()
        return super().form_valid(form)

class Main(ListView):
    model = Cover
    template_name = 'app_media/main.html'
    context_object_name = 'entres'


class CoverList(ListView):
    model = Cover
    template_name = 'app_media/cover_list.html'
    context_object_name = 'entres'
    queryset = Cover.objects.all().order_by('-created_at')


class MusicList(ListView):
    model = Music
    template_name = 'app_media/music_list.html'
    context_object_name = 'entres'
    queryset = Cover.objects.all().order_by('-created_at')


class TextList(ListView):
    model = MusicText
    template_name = 'app_media/text_list.html'
    context_object_name = 'entres'
    queryset = Cover.objects.all().order_by('-created_at')


class CoverDetail(DetailView):
    model = Cover
    template_name = 'app_media/cover_detail.html'
    context_object_name = 'entry'


class MusicDetail(DetailView):
    model = Music
    template_name = 'app_media/music_detail.html'
    context_object_name = 'entry'


class TextDetail(DetailView):
    model = MusicText
    template_name = 'app_media/text_detail.html'
    context_object_name = 'entry'


class UploadCover(LoginRequiredMixin, FormView):
    form_class = CoverForm
    template_name = 'app_media/cover_create.html'
    success_url = '/main'

    def form_valid(self, form):
        entry = Cover.objects.create(user=self.request.user,
                                     name=self.request.POST['name'],
                                     description=self.request.POST['description'],
                                     price=self.request.POST['price'])

        entry_image = CoverImage.objects.create(entry=entry, image=self.request.FILES['images'])
        entry_image.save()
        return redirect('/main')


class UploadMusic(LoginRequiredMixin, FormView):
    form_class = MusicForm
    template_name = 'app_media/music_create.html'
    success_url = '/main'

    def form_valid(self, form):
        entry = Music.objects.create(user=self.request.user,
                                     name=self.request.POST['name'],
                                     description=self.request.POST['description'],
                                     price=self.request.POST['price'],
                                     genre=self.request.POST['genre'])

        entry_file = MusicSound.objects.create(entry=entry, file=self.request.FILES['files'])
        entry_file.save()
        return redirect('/main')


class UploadText(LoginRequiredMixin, FormView):
    form_class = TextForm
    template_name = 'app_media/text_create.html'
    success_url = '/main'

    def form_valid(self, form):
        entry = MusicText.objects.create(user=self.request.user,
                                         name=self.request.POST['name'],
                                         text=self.request.POST['text'],
                                         price=self.request.POST['price'],
                                         style=self.request.POST['style'])
        return redirect('/main')

