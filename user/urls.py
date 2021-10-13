from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views


urlpatterns = [
    path('register/',views.registerUser),
    path('profile/',views.user_profile),
    path('update/',views.user_update,name='user_update'),
    path('password/',views.change_password,name='change_password'),
    path('orders/',views.orders,name='orders'),
    path('orderdetail/<int:id>',views.order_detail,name='orders'),
    path('comments/',views.comments,name='comments'),
    path('deletecomment/<int:id>',views.deletecomment,name='deletecomment'),
    path('product_create/',views.product_create,name='product_create'),
    path('favorites/<int:id>',views.add_favorites,name='add_favorites'),
    path('favorites/',views.favorite_list,name='favorite_list'),
]