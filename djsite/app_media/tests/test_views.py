from django.test import TestCase, RequestFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from app_media.models import Profile, Entry, EntryImage
from django.contrib.auth.models import User
from app_media.views import Update
from pathlib import Path, PurePath

NUMBER_OF_ITEMS = 10

class LoginLogoutTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='test123', email='passwordTest123@bk.ru', password='passwordTest123')


    def test_login(self):
        response = self.client.post('/login/', {'username': 'test123', 'password': 'passwordTest123'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_active)
        self.assertEqual(response.context['user'].email, 'passwordTest123@bk.ru')

    def test_logout(self):
        response = self.client.post('/login/', {'username': 'test123', 'password': 'passwordTest123'}, follow=True)
        response = self.client.post('/logout/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'AnonymousUser')



class RegisterTest(TestCase):
    def test_register_user(self):
        data = {
            'username': 'test123',
            'email': 'passwordTest123@bk.ru',
            'password1': 'passwordTest123',
            'password2': 'passwordTest123',
            'number': 891234567,
            'city': 'Moskow'
        }
        response = self.client.post('/register/', data)
        user = User.objects.get(username=data['username'])
        login_user = self.client.login(username='test123', password='passwordTest123')
        self.assertIsInstance(user, User)
        self.assertTrue(login_user)

class MainUpdateTest(TestCase):
    def setUp(self) -> None:
        data = {
            'username': 'test123',
            'email': 'passwordTest123@bk.ru',
            'password1': 'passwordTest123',
            'password2': 'passwordTest123',
            'number': 891234567,
            'city': 'Moskow'
        }
        response = self.client.post('/register/', data)

    def test_update(self):
        user_id = 1
        user = User.objects.get(id=user_id)
        data_2 = {
            'first_name': 'test123_new',
            'last_name': 'test_new',
            'email': 'passwordTest123_new@bk.ru',
            'number': 5555555,
            'city': 'New'
        }
        response = self.client.post(f'/update/{user_id}', data_2, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_active)
        self.assertEqual(response.context['user'].email, 'passwordTest123_new@bk.ru')
        self.assertEqual(response.context['user'].profile.city, 'New')


    def test_main(self):
        response = self.client.get('/main/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_media/main.html')


class DetailContextTest(TestCase):
    def setUp(self) -> None:
        data = {
            'username': 'test123',
            'email': 'passwordTest123@bk.ru',
            'password1': 'passwordTest123',
            'password2': 'passwordTest123',
            'number': 891234567,
            'city': 'Moskow'
        }
        response = self.client.post('/register/', data)
        response = self.client.post('/login/', {'username': 'test123', 'password': 'passwordTest123'}, follow=True)

    def test_context(self):
        data = {
            'first_name': 'test123_new',
            'last_name': 'test_new',
            'email': 'passwordTest123_new@bk.ru',
            'number': 5555555,
            'city': 'New'
        }
        response = self.client.post('/update/1', data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].first_name, 'test123_new')
        self.assertEqual(response.context['user'].profile.number, 5555555)
        self.assertEqual(response.context['user'].profile.city, 'New')


class EntryTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        for item_index in range(NUMBER_OF_ITEMS):
            Entry.objects.create(name=f'Запись {item_index}', description=f'Описание записи {item_index}')

    def test_exist_entry_list(self):
        response = self.client.get('/entres/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_media/entry_list.html')

    def test_entry_count(self):
        response = self.client.get('/entres/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['entres']) == NUMBER_OF_ITEMS)

    def test_one_entry(self):
        response = self.client.get('/entry_detail1/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_media/entry_detail.html')
        self.assertEqual(response.context['object'].name, 'Запись 0')

class UploadTest(TestCase):
    def setUp(self) -> None:
        user = User.objects.create_user(username='test123', email='passwordTest123@bk.ru', password='passwordTest123')
        response = self.client.post('/login/', {'username': 'test123', 'password': 'passwordTest123'}, follow=True)

    def test_upload_entry(self):
        cwd = Path.cwd()
        image_jpg = open(PurePath.joinpath(cwd, 'app_media', 'tests', 'tests_file', 'image.jpg'), "rb")
        image = SimpleUploadedFile(image_jpg.name, image_jpg.read())
        response = self.client.post('/upload_entry/', {'name': 'Запись', 'description': 'Описание', 'images': image}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(EntryImage.objects.all().count(), 1)