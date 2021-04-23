import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from oauth2_provider.models import get_application_model

Application = get_application_model()

class UserTest(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        application = Application.objects.first()
        username = "wilkeralves"
        password = "admin"

        token_request_data = {
            "grant_type": "password",
            "client_id": f"{application.client_id}",
            "client_secret": f"{application.client_secret}",
            "username": username,
            "password": password
        }

        auth_headers = {
            "CONTENT-TYPE": "application/x-www-form-urlencoded"
        }

        response = self.client.post(reverse("oauth2_provider:token"), data=token_request_data, **auth_headers)
        if response.status_code == 200:
            content = json.loads(response.content.decode("utf-8"))
            access_token = content["access_token"]
            self.auth_headers = {
                "HTTP_AUTHORIZATION": "Bearer " + access_token,
            }

    def test_login_user_correct(self):
        application = Application.objects.first()
        username = "wilkeralves"
        password = "admin"

        token_request_data = {
            "grant_type": "password",
            "client_id": f"{application.client_id}",
            "client_secret": f"{application.client_secret}",
            "username": username,
            "password": password
        }

        auth_headers = {
            "CONTENT-TYPE": "application/x-www-form-urlencoded"
        }

        response = self.client.post(reverse("oauth2_provider:token"), data=token_request_data, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_user_incorrect(self):
        application = Application.objects.first()
        username = "wilkeralves"
        password = "teste"

        token_request_data = {
            "grant_type": "password",
            "client_id": f"{application.client_id}",
            "client_secret": f"{application.client_secret}",
            "username": username,
            "password": password
        }

        auth_headers = {
            "CONTENT-TYPE": "application/x-www-form-urlencoded"
        }

        response = self.client.post(reverse("oauth2_provider:token"), data=token_request_data, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_users(self):
        expected = [{'id': 1, 'username': 'wilkeralves', 'email': 'wilker.ba@hotmail.com'}, {'id': 2, 'username': 'usuario_comum', 'email': 'usuario_comum@gmail.com'}]

        response = self.client.get(reverse('user-list'), **self.auth_headers)
        response.status_code == 200
        content = json.loads(response.content.decode("utf-8"))
        # import ipdb
        # ipdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content['results'], expected)

    def test_list_users(self):
        expected = [{'id': 1, 'username': 'wilkeralves', 'email': 'wilker.ba@hotmail.com'}, {'id': 2, 'username': 'usuario_comum', 'email': 'usuario_comum@gmail.com'}]

        response = self.client.get(reverse('user-list'), **self.auth_headers)
        response.status_code == 200
        content = json.loads(response.content.decode("utf-8"))
        # import ipdb
        # ipdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content['results'], expected)