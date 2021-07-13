from django.test import TestCase, SimpleTestCase
from django.urls import resolve, reverse
from app import views


class UrlsTests(SimpleTestCase):

    def test_main_url_is_resolved(self):
        url = reverse("main")
        self.assertEquals(resolve(url).func, views.main)

    def test_legals_url_is_resolved(self):
        url = reverse("legal_notice")
        self.assertEquals(resolve(url).func, views.get_legal_notice)
    
    def test_contact_url_is_resolved(self):
        url = reverse("contact")
        self.assertEquals(resolve(url).func, views.get_contact)

    # def test_explore_url_is_resolved(self):
    #     url = reverse("explore")
    #     self.assertEquals(resolve(url).func, views.SearchResults)

    def test_substitutes_url_is_resolved(self):
        url = reverse("substitutes", kwargs={"product_id": 1})
        self.assertEquals(resolve(url).func, views.get_substitutes)

    def test_product_url_is_resolved(self):
        url = reverse("product", kwargs={"product_id": 1})
        self.assertEquals(resolve(url).func, views.get_product_details)

    def test_add_favorite_url_is_resolved(self):
        url = reverse("add_favorite", kwargs={"product_id": 1})
        self.assertEquals(resolve(url).func, views.add_favorite)

    def test_favorites_url_is_resolved(self):
        url = reverse("favorites",)
        self.assertEquals(resolve(url).func, views.favorites_list)

    # py manage.py test
