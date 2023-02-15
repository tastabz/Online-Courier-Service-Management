from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse, resolve
import users.views as user_views


# Create your tests here.


class TestUrls(SimpleTestCase):

    def test_home_resolved(self):
        url = reverse('users:home')
        print(resolve(url))
        self.assertEqual(resolve(url).func, user_views.home)


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.home = reverse('users:home')

    def test_customer_signup(self):
        client = Client()
        response = client.get(reverse('users:customer_signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/customer_form.html')

    def test_customer_login(self):
        client = Client()
        response = client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_customer_logout(self):
        client = Client()
        response = client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registrations/logged_out.html')

    def test_customer_detail(self):
        client = Client()
        response = client.get(reverse('users:customer_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/customer_detail.html')

    def test_customer_update(self):
        client = Client()
        response = client.get(reverse('users:customer_update'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/customer_update.html')

    def test_customer_password_reset(self):
        client = Client()
        response = client.get(reverse('users:password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_reset.html')
