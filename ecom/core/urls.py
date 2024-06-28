from django.urls import path
from .views import CreateUserView, LoginView, AddToCartView, RemoveFromCartView, CountItemsView, ResetCartView, UpdateCartItemView


urlpatterns = [
    path('register', CreateUserView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('cart/add', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/remove/<int:pk>', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('cart/count', CountItemsView.as_view(), name='cart-item-count'),
    path('cart/reset', ResetCartView.as_view(), name='reset-cart'),
    path('cart/update/<int:pk>', UpdateCartItemView.as_view(), name='update-cart-item'),
]