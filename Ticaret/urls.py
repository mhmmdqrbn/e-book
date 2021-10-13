"""Ticaret URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from collections import namedtuple
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static
from home import views
from order import views as orderviews




urlpatterns = [
    path('',include('home.urls')),
    path('home/',include('home.urls')),
    path('product/',include('product.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('user/',include('user.urls')),
    path('order/',include('order.urls')),
    path('content/',include('content.urls')),
    path('admin/', admin.site.urls),


    path('error/',views.page_error,name='error'),
    path('content/<int:id>/<slug:slug>',views.contentdetail,name='contentdetail'),
    path('menu/<int:id>',views.menu,name='menu'),
    path('aboutus',views.aboutus,name='aboutus'),
    path('references',views.references,name='references'),
    path('contact',views.contact,name='contact'),
    path('category/<int:id>/<slug:slug>/',views.category_products,name='category_products'),
    path('product/<int:id>/<slug:slug>/',views.product_detail,name='product_detail'),
    path('search/',views.product_search,name='product_search'),
    path('search_auto/',views.product_search_auto,name='product_search_auto'),
    path('logout/',views.logoutUser,name='logoutUser'),
    path('login/',views.loginUser,name='loginUser'),
    path('shopcart/',orderviews.shopcart,name='shopcart'),
    path('faq/',views.faq,name='faq'),
    path('shop/',views.shop , name= 'shop')
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
