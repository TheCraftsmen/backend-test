from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from orders.models import Menu, Options

User = get_user_model()


class OrderTestCase(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create(
            username='blas',
            password='cornershop',
            is_staff=True
        )
        self.user = User.objects.create(
            username='pepo',
            password='cornershop'
        )
        self.menu = Menu.objects.create(date='2019-04-17')
        for i, option in enumerate(["pizza", "paty", "milanesa", "chorizo vegano"]):
            o = Options()
            o.option_id = i
            o.text = option
            o.menu = self.menu
            o.save()

    def test_create_order_without_auth(self):
        url = reverse('order')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_order_no_body(self):
        url = reverse('order')
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order(self):
        url = reverse('order')
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, format='json', data={
            'option_selected': 1,
            'menu': self.menu.id
        })
        created_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # create again a new order
        response = self.client.post(url, format='json', data={
            'option_selected': 1,
            'menu': self.menu.id
        })
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(data['non_field_errors'][0], 'Already selected menu!')

        # delete order
        url = reverse('order_detail', kwargs={'pk': created_data['id']})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # test customizations text
        url = reverse('order')
        response = self.client.post(url, format='json', data={
            'option_selected': 1,
            'menu': self.menu.id,
            'customizations': 'sin lechuga'
        })
        created_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(created_data['customizations'], 'sin lechuga')

        # modify order
        url = reverse('order_detail', kwargs={'pk': created_data['id']})
        response = self.client.patch(url, format='json', data={
            'customizations': 'sin queso',
            'option_selected': 1,
            'menu': self.menu.id,
        })
        patch_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_data['customizations'], 'sin queso')

        # test get order
        url = reverse('order')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # test get order detail
        url = reverse('order_detail', kwargs={'pk': created_data['id']})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MenuTestCase(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create(
            username='blas',
            password='cornershop',
            is_staff=True
        )
        self.user = User.objects.create(
            username='pepo',
            password='cornershop'
        )
        self.menu = Menu.objects.create(date='2019-04-16')
        for i, option in enumerate(["pizza", "paty", "milanesa", "chorizo vegano"]):
            o = Options()
            o.option_id = i
            o.text = option
            o.menu = self.menu
            o.save()

    def test_create_menu_without_auth(self):
        url = reverse('menu')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_menu_without_admin_api(self):
        url = reverse('menu')
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_menu_without_auth_in_admin_api(self):
        url = reverse('admin_menu')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_menu_without_admin_account_in_admin_api(self):
        url = reverse('admin_menu')
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_menu_no_data(self):
        url = reverse('admin_menu')
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_menu(self):
        url = reverse('admin_menu')
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(url, format='json', data={
            "date": '2019-04-17',
            "options": [
                {
                    "text": "pizza"
                },
                {
                    "text": "milanesa"
                },
                {
                    "text": "hamburguesa"
                },
                {
                    "text": "tortilla"
                }
            ]
        })
        created_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # delete menu
        url = reverse('admin_menu_detail', kwargs={'pk': created_data['id']})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_today_menu_without_auth(self):
        url = reverse('menu_detail', kwargs={'pk': self.menu.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
