from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.test import TestCase
from .models import Cart, CartItem
from django.contrib.auth.models import User


class AuthenticationTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        }

    def test_user_registration(self):
        response = self.client.post(self.register_url,
                                    self.user_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        self.client.post(self.register_url, self.user_data, format='json')
        response = self.client.post(self.login_url,
                                    self.user_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)

class CartAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.client.login(username='testuser', password='testpassword123')
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(cart=self.cart, product_id=123, quantity=2)
    
    def test_add_to_cart(self):
        url = reverse('add-to-cart')
        response = self.client.post(url, {'product_id': 124, 'quantity': 1})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.count(), 2)
    
    def test_remove_from_cart(self):
        url = reverse('remove-from-cart', args=[123])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CartItem.objects.count(), 0)
    
    def test_count_items(self):
        url = reverse('count-items')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
    
    def test_reset_cart(self):
        url = reverse('reset-cart')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CartItem.objects.count(), 0)
    
    def test_update_item_count(self):
        url = reverse('update-item', args=[123])
        response = self.client.patch(url, {'quantity': 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cart_item.refresh_from_db()
        self.assertEqual(self.cart_item.quantity, 5)