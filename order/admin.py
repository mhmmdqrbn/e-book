from django.contrib import admin
from order.models import Order, OrderProduct, ShopCart
# Register your models here.


class ShopCartAdmin(admin.ModelAdmin):
    list_display=['user','product','price','quantity','amount']
    list_filter = ['user']

class OrderProductLine(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('user','product','price','quantity','amount')
    can_delete = False
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display=['code','first_name','last_name','phone','city','total','status']
    list_filter = ['status']
    readonly_fields = ('user','address','city','country','phone','first_name','ip','last_name','phone','total')
    can_delete = False
    inlines = [OrderProductLine]

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['user','product','price','quantity','amount']
    list_filter = ['user']

admin.site.register(ShopCart,ShopCartAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct,OrderProductAdmin)

