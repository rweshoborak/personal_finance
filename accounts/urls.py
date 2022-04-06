from django.urls import path
from . import views
app_name = 'accounts'
urlpatterns = [
    path('login', views.loginPage, name='login'),
    path('register', views.registrerPage, name='register'),
    path('logout', views.logoutUser, name='logout'),

    path('user', views.userPage, name = 'userpage'),
    path('account',views.accountSettings, name='account'),


    path('', views.home, name='home'),
    path('product', views.products, name='products'),
    path('customer/<str:pk>', views.customer, name='customer'),

    path('create_order/<str:pk>', views.create_order, name='create_order'),
    path('update_order<str:pk>', views.update_order, name='update_order'),
    path('delete_order/<str:pk>', views.delete_order, name='delete_order'),

    path('add_product', views.add_product, name='add_product'),
    path('update_product/<str:pk>', views.update_product, name='update_product'),
    path('delete_product/<str:pk>', views.delete_product, name='delete_product'),



]
