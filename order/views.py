from django.contrib.auth import login
from django.http import request
from order.models import Order, OrderForm, OrderProduct, ShopCart, ShopCartForm
import django
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from product.models import Category, Product
from home.models import UserProfile
from django.utils.crypto import get_random_string

# Create your views here.


def index(request):
    return HttpResponse('Sifaris')

@login_required(login_url='/login') # Login yoxlanmasi
def addtocart(request,id):
    url = request.META.get('HTTP_REFERER') # Sonuncu url almaq
    current_user = request.user # Hazirki istifadeci
    checkcart = ShopCart.objects.filter(product_id = id) # Sebetin yoxlanmasi ucun 
    if checkcart:
        control = 1 # Mehsul sebetde var
    else:
        control = 0 # Mehsul sebetde yoxdur

    
    if request.method == 'POST': # form post edilibse
        form = ShopCartForm(request.POST)
        if form.is_valid():

            if control == 1: #Mehsul varsa ustune elave et
                data = ShopCart.objects.get(product_id = id)
                data.quantity += form.cleaned_data['quantity']
                data.save() # sql e save et


            else: #Mehsul yoxsa elave et
                data = ShopCart() #modeli dataya baglamaq
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save() #sql save et
                # Sebetdeki mehsullarin sayimi ucun
                request.session['cart_items'] = ShopCart.objects.filter(user_id = current_user.id).count()
                messages.success(request,'Kitab səbətə əlavə olundu.')
                return HttpResponseRedirect(url)

    else: # Mehsul bir basa sebete elave olunarsa


        if control == 1: #Mehsul varsa ustune elave et
            data = ShopCart.objects.get(product_id = id)
            data.quantity += 1
            data.save() # sql e save et


        else: # Mehsul yoxdursa elave edir
            data = ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.save()
            request.session['cart_items'] = ShopCart.objects.filter(user_id = current_user.id).count()
            messages.success(request,'Kitab səbətə əlavə olundu.')
            return HttpResponseRedirect(url)


    messages.warning(request,'Kitab səbətə yüklənmədi.')
    return HttpResponseRedirect(url)



@login_required(login_url='/login') # Login yoxlanmasi
def shopcart(request):
    category = Category.objects.all()
    current_user = request.user
    schopcart = ShopCart.objects.filter(user_id = current_user.id)
    request.session['cart_items'] = ShopCart.objects.filter(user_id = current_user.id).count()
    total = 0

    for data in schopcart:
        total += data.product.price * data.quantity

    context = {
        'schopcart':schopcart,
        'category':category,
        'total':total
    }

    return render(request,'shopcart_products.html',context)


@login_required(login_url='/login') # Login yoxlanmasi
def deletefromcart(request,id):
    ShopCart.objects.filter(id = id).delete()
    current_user = request.user
    request.session['cart_items'] = ShopCart.objects.filter(user_id = current_user.id).count()

    messages.success(request,'Kitab səbətdən silinmişdir.')
    return HttpResponseRedirect('/shopcart')
    

@login_required(login_url='/login') # Login yoxlanmasi
def orderproduct(request):
    category = Category.objects.all() #kategoriya aid her seyi almaq
    current_user = request.user # login olan user
    schopcart = ShopCart.objects.filter(user_id = current_user.id) #shop karta login olan useri tanimlamaq
    total = 0
    for rs in schopcart:
        total += rs.product.price * rs.quantity

    if request.method == 'POST': #Eger post varsa
        form = OrderForm(request.POST)

        if form.is_valid():
            # Kart melumatlarini al ve banka gonder 
            data = Order()
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper()    # RANDOM KOD
            data.code = ordercode
            data.save()


            schopcart = ShopCart.objects.filter(user_id = current_user.id)
            for rs in  schopcart:
                detail = OrderProduct()
                detail.order_id = data.id
                detail.product_id = rs.product_id
                detail.user_id = current_user.id
                detail.quantity = rs.quantity
                detail.price = rs.product.price
                detail.amount = rs.amount
                detail.save()

                
                product = Product.objects.get(id = rs.product_id)
                product.amount -= rs.quantity
                product.save()

        
            ShopCart.objects.filter(user_id = current_user.id).delete()
            request.session['cart_items']=0
            return render(request,'Order_Completed.html',{'ordercode':ordercode ,'category':category})
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/order/orderproduct')


    form = OrderForm()
    profile = UserProfile.objects.get(user_id = current_user.id)
    context = {
        'schopcart':schopcart,
        'category':category,
        'total':total,
        'form':form,
        'profile':profile
    }

    return render(request,'Order_Form.html',context)
