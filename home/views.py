from content.models import CImages, Content, Menu
from home.forms import SearchForm
from django.contrib import messages
from home.models import   FAQ, ContactForm, ContactFormMessage, Setting
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from product.models import Category, Comment, Product
import json
from django.contrib.auth import logout,login,authenticate
from home.models import UserProfile
from order.models import ShopCart
from django.core.paginator import Paginator

# Create your views here.


def index(request):
    current_user = request.user
    setting = Setting.objects.get()
    sliderdata = Product.objects.all()[:6]
    category = Category.objects.all()
    products = Product.objects.all()
    dayproducts = Product.objects.all().order_by('-product_view')[:5]
    lastproducts = Product.objects.all().order_by('-id')[:4]
    randomproducts = Product.objects.all().order_by('price')[:4]
    news = Content.objects.filter(type='xəbər').order_by('-id')[:4]
    announcement = Content.objects.filter(type='endirim').order_by('-id')[:4]
    request.session['cart_items'] = ShopCart.objects.filter(user_id = current_user.id).count()
    userprofil = UserProfile.objects.all()
    schopcart = ShopCart.objects.filter(user_id = current_user.id)
    total = 0
    for data in schopcart:
        total += data.product.price * data.quantity


    context = {
        'setting':setting,
        'page':'home',
        'category':category,
        'sliderdata':sliderdata,
        'dayproducts':dayproducts,
        'lastproducts':lastproducts,
        'randomproducts':randomproducts,
        'userprofil':userprofil,
        'total':total,
        'news':news,
        'announcement':announcement,
        'products':products
        
    }
    return render(request,'index.html',context)


def aboutus(request):
    current_user = request.user
    schopcart = ShopCart.objects.filter(user_id = current_user.id)
    total = 0
    setting = Setting.objects.get()
    category = Category.objects.all()

    for data in schopcart:
        total += data.product.price * data.quantity
    context = {
        'setting':setting,
        'category':category,
        'total':total
    }
    return render(request,'aboutus.html',context)


def references(request):
    current_user = request.user
    schopcart = ShopCart.objects.filter(user_id = current_user.id)
    total = 0
    setting = Setting.objects.get()
    category = Category.objects.all()

    for data in schopcart:
        total += data.product.price * data.quantity
    context = {
        'setting':setting,
        'category':category,
        'total':total
    }
    return render(request,'references.html',context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST or None)
        if form.is_valid():
            data = ContactFormMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.save()
            messages.info(request,'Mesajınız göndərilmişdir.')
            return HttpResponseRedirect('/contact')

    current_user = request.user
    schopcart = ShopCart.objects.filter(user_id = current_user.id)
    total = 0
    setting = Setting.objects.get()
    category = Category.objects.all()
    form = ContactForm()
    for data in schopcart:
        total += data.product.price * data.quantity

    context = {
        'setting':setting,
        'form':form,
        'category':category,
        'total':total
    }

    return render(request,'contact.html',context)


def category_products(request,id,slug):
    products = Product.objects.filter(category_id=id)
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    setting = Setting.objects.get()
    current_user = request.user
    schopcart = ShopCart.objects.filter(user_id = current_user.id)
    total = 0
    menu = Menu.objects.all()
    for data in schopcart:
        total += data.product.price * data.quantity

    context = {
        'setting':setting,
        'products':products,
        'category':category,
        'slug':slug,
        'categorydata':categorydata,
        'total':total,
    }

    return render(request,'products.html',context)


def product_detail(request,id,slug):
    # try:
        category = Category.objects.all()
        salam = Product.objects.get(id=id)
        product = Product.objects.get(pk=id)
        comments = Comment.objects.filter(product_id=id)
        cem = 0
        paginator =  Paginator(comments,3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        product.product_view += 1
        

        status = salam.status
        stok = salam.amount
        

        for i in comments:
            cem += int(i.rate)
        

        if cem==0:
            cem =5  
        else:
            cem = cem//len(comments)
        product.save()
        context = {
            'category':category,
            'product':product,
            'slug':slug,
            'comments':comments,
            "cem":cem,
            "cemrange":range(cem),
            "cemrange2":range(5-cem),
            'status':status,
            'stok':stok,
            'page_obj':page_obj
            
        }
        
        return render(request,'product_detail.html',context)
    # except:
    #     link='/error'
    #     return HttpResponseRedirect(link)


def product_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            setting = Setting.objects.get()
            category = Category.objects.all()
            query = form.cleaned_data['query']
            katid = form.cleaned_data['katid']
            if katid == 0:
                products = Product.objects.filter(title__icontains = query)
            else:
                products = Product.objects.filter(title__icontains = query , category_id = katid)



            context = {
                'category':category,
                'products':products,
                'setting':setting
                
            }
            return render(request,'products_search.html',context)
    return HttpResponseRedirect('/')


def product_search_auto(request):
  if request.is_ajax():
        q = request.GET.get('term', '')
        product = Product.objects.filter(title__icontains=q)
        results = []
        for rs in product:
            product_json = {}
            product_json = rs.title
            results.append(product_json)
        data = json.dumps(results)
  else:
        data = 'fail'
  mimetype = 'application/json'
  return HttpResponse(data, mimetype)


def logoutUser(request):
    logout(request)

    return HttpResponseRedirect('/')


def loginUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username = username , password = password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request,'Daxil olma xətası / username və ya şifrə yanlışdır!')
            return HttpResponseRedirect('/login')

    category = Category.objects.all()
    context = {
    'category':category,
    }

    return render(request,'login.html',context)


def menu(request,id):
    try:
        content = Content.objects.get(menu_id=id)
        link = '/content/'+ str(content.id)+'/menu'
        return HttpResponseRedirect(link)
    except:
        messages.warning(request,'Xəta! Əlaqəli məlumat tapılmadı!')
        link='/error'
        return HttpResponseRedirect(link)

def contentdetail(request,id,slug):
    category = Category.objects.all()
    menu = Menu.objects.all()

    # try:
    content = Content.objects.all()
    images = CImages.objects.filter(content_id = id)
    product = Product.objects.all()

    context = {
        'content':content,
        'category':category,
        'menu':menu,
        'images':images,
    }
    return render(request,'product_detail.html',context)
    # except:
        # link='/error'
        # return HttpResponseRedirect(link)

def page_error(request):

    category = Category.objects.all()


    context = {
        'category':category,
    }
    return render(request,'error.html',context)


def faq(request):
    category = Category.objects.all()
    faq = FAQ.objects.all().order_by('ordernumber')
    setting = Setting.objects.get()

    context = {
        'category':category,
        'faq':faq,
        'setting':setting
    }
    return render(request,'faq.html',context)

def shop(request):
    category = Category.objects.all()
    setting = Setting.objects.get()
    product = Product.objects.all()
    request.session['comment_item']=0
    comment_count = Comment.objects.all().count()
    paginator =  Paginator(product,6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category':category,
        'product':product,
        'setting':setting,
        'comment':comment_count,
        'page_obj':page_obj
    }
    return render(request,'shop.html',context)


# def registerUser(request):
#     if request.method == 'POST':
#         form = registerForm(request.Post)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(username = username , password = password)
#             login(request,user)
#             return HttpResponseRedirect('/')
#     form = registerForm()
#     category = Category.objects.all()
#     context = {
#     'category':category,
#     'form':form
#     }

#     return render(request,'register.html',context)