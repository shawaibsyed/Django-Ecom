from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from .models import Cart, CartItem, Product, OrderItem, Order


class CreateUserView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'error': 'Username and password required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, password=password)
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response({'error': u'Username "%s" is already in use.' % username}, status=status.HTTP_400_BAD_REQUEST)
        

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                # 'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
class AddToCartView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        product_name = request.data['product_name']
        quantity = request.data['quantity']
        try:
            product = Product.objects.get(product_name=product_name)
        except Product.DoesNotExist: 
            return Response({
                "message": "Product Name Invalid!"
            }, status=status.HTTP_400_BAD_REQUEST) 
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                user = request.user
            )
        cart.save()

        try:
            cart_item = CartItem.objects.get(product_id=product_name, cart=cart)
            cart_item.quantity += quantity
            cart_item.save()
            
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product_id = product,
                quantity = quantity,
                cart = cart,
            )
            cart_item.save()    
        response_data = {
                "message": "Item successfully added to cart!"
            }
        return Response(response_data)

class RemoveFromCartView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk):
        product_name = request.data['product_name']
        quantity = request.data['quantity']
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                user = request.user
            )
        cart.save()
        try:
            cart_item = CartItem.objects.get(id=pk, cart=cart)
            cart_item.delete()
            
        except CartItem.DoesNotExist:   
            return Response({
                "message": "Cart Item doesn't exists!"
            }, status=status.HTTP_400_BAD_REQUEST)
        response_data = {
                "message": "Item successfully removed!"
            }
        return Response(response_data)

class CountItemsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                user = request.user
            )
        cart.save()
        count = cart.items.count()
        return Response({'count': count})

class ResetCartView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def delete(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                user = request.user
            )
        cart.save()
        cart.items.all().delete()
        response_data = {
                "message": "Cart Reset Successfully!"
            }
        return Response(response_data)

class UpdateCartItemView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def patch(self, request, pk):
        product_name = request.data['product_name']
        quantity = request.data['quantity']
        try:
            product = Product.objects.get(product_name=product_name)
        except Product.DoesNotExist: 
            return Response({
                "message": "Product Name Invalid!"
            }, status=status.HTTP_400_BAD_REQUEST) 
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                user = request.user
            )
        cart.save()
        if quantity<0:
           return Response({
                "message": "Please enter a valid quantity!"
            }, status=status.HTTP_400_BAD_REQUEST) 
        try:
            cart_item = CartItem.objects.get(id=pk, cart=cart)
            cart_item.quantity = quantity
            cart_item.save()
            
        except CartItem.DoesNotExist:   
            return Response({
                "message": "Cart Item doesn't exists!"
            }, status=status.HTTP_400_BAD_REQUEST)
        response_data = {
                "message": "Item successfully updated!"
            }
        return Response(response_data)
    

class CartCheckoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                user = request.user
            )
        cart.save()
        order = Order.objects.create(
            user = request.user
        )
        order.save()
        order_items = []
        price = 0
        for item in cart.items.all():
            order_items.append(OrderItem.objects.create(
                product_id=item.product_id,
                quantity=item.quantity,
                order=order
                ))
            price += item.product_id.price * item.quantity
            order_items[-1].save()
        order.price = round(price,2)
        order.save()
        cart.items.all().delete()
        response_data = {
                "message": "Order Placed, Thank You!!"
            }
        return Response(response_data)
    