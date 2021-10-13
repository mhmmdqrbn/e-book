from django.urls import path
from django.urls.conf import include
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('addcomment/<int:id>',views.addcomment,name='addcomment')
]
