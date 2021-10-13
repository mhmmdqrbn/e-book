from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from order.models import Order, OrderProduct, ShopCart
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from user.forms import  ProfileUpdateForm, RegisterForm, UserUpdateForm
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import login, update_session_auth_hash
from product.models import Category, Comment, Product
from home.models import Setting, UserProfile



# Create your views here.
def registerUser(request):
    
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        confirm = form.cleaned_data.get('confirm')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        email = form.cleaned_data.get('email')

        # newUser = User(username = username, first_name = first_name , last_name = last_name , email = email)
        # newUser.set_password(password)
        try:
                category = Category.objects.all()
                newUser= User.objects.get(username=username)
                context= {'form': form, 'error':'İstifadəçi adı artıq var!','category':category}
                return render(request, 'register.html', context)
        except User.DoesNotExist:
                newUser = User(username = username, first_name = first_name , last_name = last_name , email = email)

                newUser.save()
                login(request,newUser)

                current_user = request.user
                data = UserProfile()
                data.user_id = current_user.id
                data.image = 'images/users/user.png'
                data.save()

                return HttpResponseRedirect('/')
    category = Category.objects.all()
    context = {
        'form':form,
        'category':category
    }
    return render(request,'register.html',context)

@login_required(login_url='/login')
def user_profile(request):
    category = Category.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id = current_user.id)

    context = {
        'category':category,
        'profile':profile,
    }

    return render(request,'user_profile.html',context)

@login_required(login_url='/login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST , instance = request.user)
        profile_form = ProfileUpdateForm(request.POST , request.FILES , instance = request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Profiliniz yenilenmisdir!')
            return redirect('/user/profile')

    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance = request.user)
        profile_form = ProfileUpdateForm(instance = request.user.userprofile)
        context = {
            'category':category,
            'user_form':user_form,
            'profile_form':profile_form
        }
        return render(request,'user_update.html',context)

@login_required(login_url='/login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)
            messages.success(request,'Paarol deyisdi')
        else:
            messages.error(request,'Duzgun daxil edin' + str(form.errors))
            return HttpResponseRedirect('/user/password')

    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request,'change_password.html',{'form':form,'category':category})


@login_required(login_url='/login')
def orders(request):
    category = Category.objects.all()
    current_user = request.user
    orders = Order.objects.filter(user_id = current_user.id)
    context = {
        'category':category,
        'orders':orders,
    }
    return render(request,'user_orders.html',context)

@login_required(login_url='/login')
def order_detail(request,id):
    category = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id = current_user.id,id=id)
    orderItems = OrderProduct.objects.filter(order_id = id)

    context = {
        'category':category,
        'order':order,
        'orderItems':orderItems,
    }
    return render(request,'user_order_detail.html',context)

@login_required(login_url='/login')
def comments(request):
    category = Category.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id = current_user.id)
    

    context = {
        'category':category,
        'comments':comments,
    }
    return render(request,'user_comments.html',context)

def deletecomment(request,id):
    current_user = request.user
    Comment.objects.filter(id = id,user_id = current_user.id).delete()

    return redirect('/user/comments')

def product_create(request):

    if request.method == 'POST':    
        author = request.POST.get('author')
        title = request.POST.get('title')
        category_name = request.POST.get('category_name')
        slug = request.POST.get('slug')
        price = request.POST.get('price')
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        image = request.POST.get('image')
        detail = request.POST.get('detail')
        category = Category.objects.get(id=category_name) 


        product = Product(title = title , author = author ,slug = slug , price = price , amount = amount ,
        description = description , image = image , category = category , detail = detail)
        
        product.save()

    category_all = Category.objects.all()
    current_user = request.user
    setting = Setting.objects.all()
    context = {
        'category':category_all,
        'current_user':current_user,
        'setting':setting,
        }
    return render(request,'product_create.html',context)

@login_required(login_url='/login')
def add_favorites(request,id):
    product = get_object_or_404(Product, id=id)
    if product.favorite.filter(id=request.user.id).exists():
        product.favorite.remove(request.user)
    else:
        product.favorite.add(request.user)
    
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required(login_url='/login')
def favorite_list(request):
    category_all = Category.objects.all()
    
    new = Product.objects.filter(favorite=request.user)
    return render(request,'product_favorites.html',{'new':new,'category':category_all,})
    