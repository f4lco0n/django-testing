from django.http import HttpRequest
from django.urls import resolve
from django.test import TestCase
from .views import home_page
from .models import Item, List
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


class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):

        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'Pierwszy element listy'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Drugi element'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list,list_)


        saved_items = Item.objects.all()
        self.assertEquals(saved_items.count(),2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'Pierwszy element listy')
        self.assertEqual(first_saved_item.list,list_)
        self.assertEqual(second_saved_item.text, 'Drugi element')
        self.assertEqual(second_saved_item.list,list_)

class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertTemplateUsed(response,'list.html')


    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='item1',list=correct_list)
        Item.objects.create(text='item2',list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='item 1 for other_list',list=other_list)
        Item.objects.create(text='item 2 for other list',list=other_list)


        response = self.client.get('/lists/%d/' % (correct_list.id,))

        self.assertContains(response, 'item1')
        self.assertContains(response, 'item2')
        self.assertNotContains(response, 'item 1 for other_list')
        self.assertNotContains(response, 'item 2 for other_list')


    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'],correct_list)

class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        self.client.post(
            '/lists/new',
            data={'item_text': 'Nowy element listy'}
        )
        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text,'Nowy element listy')

    def test_redirects_after_POST(self):
        response = self.client.post(
            '/lists/new',
            data={'item_text': 'Nowy element listy'}
        )
        new_list = List.objects.first()
        self.assertRedirects(response,'/lists/%d/' % (new_list.id,))


class NewItemTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            '/lists/%d/add_item' % (correct_list.id,),
            data={'item_text': 'Nowy element dla istniejacej listy'}
        )

        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text,'Nowy element dla istniejacej listy')
        self.assertEqual(new_item.list,correct_list)

    def test_redirects_to_list_view(self):

        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/%d/add_item' % (correct_list.id,),
            data={'item_text': 'Nowy element dla istniejacej listy'}
        )

        self.assertRedirects(response,'/lists/%d/' % (correct_list.id,))