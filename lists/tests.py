from django.http import HttpRequest
from django.urls import resolve
from django.test import TestCase
from lists.views import home_page
from django.template.loader import render_to_string
# Create your tests here.

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEquals(found.func,home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEquals(response.content.decode(), expected_html)

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method == 'POST'
        request.POST['item_text'] = 'Nowy element listy'

        response = home_page(request)

        self.assertIn('Nowy element listy',response.content.decode())

