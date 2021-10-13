from product.models import Category, Comment, Product
from django.contrib import admin

from django.utils.html import format_html
from mptt.admin import MPTTModelAdmin,DraggableMPTTAdmin
from product.models import Category,Product,Images

# Register your models here.
class ProductImageInline(admin.TabularInline):
    model = Images
    extra = 5

class CategoryAdmin(MPTTModelAdmin):
    list_display=['title','status','image_tag']
    readonly_fields = ['image_tag']

class ImagesAdmin(admin.ModelAdmin):
    list_display=['title','product','image_tag']
    readonly_fields = ['image_tag']


class ProductAdmin(admin.ModelAdmin):
    list_display=['author','title','category','image_tag','price','status']
    readonly_fields = ['image_tag']
    inlines = [ProductImageInline]
    prepopulated_fields = {'slug':('title',)}



class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug':('title',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Product,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Product,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Bu kategoriyaya aid məhsullar.'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'

class CommentAdmin(admin.ModelAdmin):
    list_display=['subject','comment','product','user','status']


admin.site.register(Category,CategoryAdmin2)
admin.site.register(Product,ProductAdmin)
admin.site.register(Images,ImagesAdmin)
admin.site.register(Comment,CommentAdmin)