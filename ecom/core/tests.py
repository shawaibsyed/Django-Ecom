from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Cart, Product, CartItem, Order, OrderItem
from .serializers import ProductSerializer, CartSerializer

class ECommerceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.product = Product.objects.create(product_name='Laptop', category='Electronics', price=1000.0)
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(cart=self.cart, product_id=self.product, quantity=1)
        self.order = Order.objects.create(user=self.user, price=1000.0)
        self.order_item = OrderItem.objects.create(order=self.order, product_id=self.product, quantity=1)

    def test_model_str(self):
        # Ensure the string representations of the models are correct
        self.assertEqual(str(self.cart), f'{self.user.username}')
        self.assertEqual(str(self.product), 'Laptop')
        self.assertEqual(str(self.cart_item), f'{self.cart} | {self.product} | 1')
        self.assertEqual(str(self.order), f'Order for {self.user.username} at {self.order.date}')
        self.assertEqual(str(self.order_item), f'{self.order} | {self.product} | 1')

    def test_product_serializer(self):
        # Test serialization of Product
        serializer = ProductSerializer(instance=self.product)
        self.assertEqual(serializer.data, {
            'product_name': 'Laptop',
            'category': 'Electronics',
            'price': 1000.0
        })

    def test_cart_serializer(self):
        # Test serialization of Cart
        serializer = CartSerializer(instance=self.cart)
        self.assertEqual(serializer.data, {
            'id': self.cart.id,
            'user': self.user.username,
            'items': [
                {
                    'id': self.cart_item.id,
                    'cart': self.cart.id,
                    'quantity': 1,
                    'product_id': self.product.product_name
                }
            ]
        })

    def test_create_user_view(self):
        # Test user creation view
        url = reverse('register')
        data = {'username': 'newuser', 'password': 'newpassword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_view(self):
        # Test login view
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_add_to_cart_view(self):
        # Test adding to cart
        url = reverse('add-to-cart')
        data = {'product_name': 'Laptop', 'quantity': '1'}  # Convert quantity to string to mimic real-world input
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Item successfully added to cart!', response.data['message'])

    def test_remove_from_cart_view(self):
        # Test removing from cart
        url = reverse('remove-from-cart', args=[self.cart_item.id])
        data = {'product_name': 'Laptop'}  # Ensure product_name is provided
        response = self.client.delete(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Item successfully removed!', response.data['message'])