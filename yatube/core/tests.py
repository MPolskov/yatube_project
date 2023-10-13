from http import HTTPStatus

from django.test import TestCase

NOT_FOUND_TEMPLATE = 'core/404.html'


class ViewTestClass(TestCase):
    def test_error_page(self):
        response = self.client.get('/nonexist-page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateUsed(response, NOT_FOUND_TEMPLATE)
