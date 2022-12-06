from django.test import TestCase
from app_media.models import Profile, Entry, EntryImage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
import datetime
from pathlib import Path, PurePath

class ModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='test123', email='passwordTest123@bk.ru', password='passwordTest123')

    def test_profile_model(self):
        user = User.objects.get(id=1)
        Profile.objects.create(user=user, number=7777777, city='test')
        self.assertEqual(len(Profile.objects.all()), 1)

    def test_entry_model(self):
        user = User.objects.get(id=1)
        entry = Entry.objects.create(user=user, name='test', description='test_desc', created_at=datetime.date.today())
        self.assertEqual(len(Entry.objects.all()), 1)
        self.assertEqual(str(entry), 'test')
        cwd = Path.cwd()
        image_jpg = open(PurePath.joinpath(cwd, 'app_media', 'tests', 'tests_file', 'image.jpg'), "rb")
        image = SimpleUploadedFile(image_jpg.name, image_jpg.read())
        EntryImage.objects.create(entry=entry, image=image)
        self.assertEqual(len(EntryImage.objects.all()), 1)