from django.urls import path
from . import views
urlpatterns = [
     path('', views.index, name='home'),
     path('about', views.about_us, name='about'),
     path('cart', views.cart, name='cart'),
     path('add-cart', views.add_cart, name='add_cart'),
     path('remove-cart', views.remove_cart, name='remove_cart'),
     path('update-cart', views.update_cart, name='update_cart'),
     path('contact', views.contact, name='contact'),
     path('checkout', views.checkout, name='checkout'),
     path('login', views.login_user, name='login_user'),
     path('signup', views.signup_user, name='signup_user'),
     path('logout', views.logout, name='logout')
]