# posts/tests/test_urls.py
from django.contrib.auth import get_user_model
from django.test import TestCase, Client

User = get_user_model()

class StaticURLTests(TestCase):
    def setUp(self):
        # Создаем экземпляр клиента
        self.guest_client = Client()
        # Создаем пользователя
        self.user = User.objects.create_user(username='HasNoName')
        # Создаем второй клиент
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.user)


    def test_homepage(self):
        # Делаем запрос к главной странице и проверяем статус
        response = self.guest_client.get('/')
        # Утверждаем, что для прохождения теста код должен быть равен 200
        self.assertEqual(response.status_code, 200)

    def test_author(self):
        response = self.guest_client.get('/about/author/')
        self.assertEqual(response.status_code, 200)


    def test_tech(self):
        response = self.guest_client.get('/about/tech/')
        self.assertEqual(response.status_code, 200)


    def group_list(self):
        response = self.guest_client.get('/group/a/')
        self.assertEqual(response.status_code, 200)


    def profile(self):
        response = self.guest_client.get('/profile/andrey/')
        self.assertEqual(response.status_code, 200)


    def post(self):
        response = self.guest_client.get('/posts/4/')
        self.assertEqual(response.status_code, 200)


    def create(self):
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, 200)


    def test_urls(self):
        templates_url_names = {
            'posts/index.html':'/',
            'posts/group_list.html':'/group/a/',
            'posts/profile.html':'profile/andrey',
            'post/post_detail.html':'posts/4',
        }
        for template, adress in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                self.assertTemplateUsed(response, template) 