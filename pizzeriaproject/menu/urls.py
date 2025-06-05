from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# app_name = 'menu' # We are using global URL names for simplicity for now

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='menu/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('menu/', views.menu_list_view, name='menu_list'),
    path('cart/', views.view_cart_view, name='view_cart'),
    path('orders/', views.order_history_view, name='order_history'),
    path('add_to_cart/', views.add_to_cart_view, name='add_to_cart'),
    path('remove_from_cart/', views.remove_from_cart_view, name='remove_from_cart'),
    path('place_order/', views.place_order_view, name='place_order'),
] 