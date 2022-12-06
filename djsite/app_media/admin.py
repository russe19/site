from django.contrib import admin
from app_media.models import Profile, Cover, CoverImage, MusicText, Music, MusicSound


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', )

@admin.register(Cover)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(CoverImage)
class EntryImageAdmin(admin.ModelAdmin):
    pass