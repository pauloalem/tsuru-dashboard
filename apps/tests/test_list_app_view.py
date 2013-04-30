from mock import patch, Mock

from django.test import TestCase
from django.test.client import RequestFactory

from apps.views import ListApp


class ListAppViewTest(TestCase):
    def test_should_use_list_template(self):
        request = RequestFactory().get("/")
        request.session = {"tsuru_token":"admin"}
        response_mock = Mock()
        with patch('requests.get') as get:
            response_mock.status_code = 204
            get.side_effect = Mock(return_value=response_mock)
            response = ListApp().get(request)
            self.assertEqual("apps/list.html", response.template_name)

    def teste_should_get_list_of_apps_from_tsuru(self):
        request = RequestFactory().get("/")
        request.session = {"tsuru_token":"admin"}
        with patch('requests.get') as get:
            expected = [{"framework":"python","name":"pacote",
                         "repository":"git@tsuru.com:pacote.git","state":"creating"}]
            get.return_value = Mock(status_code=200, json=expected)
            response = ListApp().get(request)
            self.assertEqual([{"framework":"python","name":"pacote",
                               "repository":"git@tsuru.com:pacote.git","state":"creating"}],
                             response.context_data.get("apps"))
