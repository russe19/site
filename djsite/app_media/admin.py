from django.contrib import admin
from app_media.models import Profile, Cover, CoverImage, MusicText, Music, MusicSound, Status, Genre, Style


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', )

@admin.register(Cover)
class CoverAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(CoverImage)
class CoverImageAdmin(admin.ModelAdmin):
    list_display = ('__str__', )


@admin.register(MusicText)
class MusicTextAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(MusicSound)
class MusicSoundAdmin(admin.ModelAdmin):
    list_display = ('__str__', )


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    list_display = ('name', )