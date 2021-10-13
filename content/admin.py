from content.models import CImages, Content, Menu
from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
# Register your models here.

class ContentImageInline(admin.TabularInline):
    model=CImages
    extra=3

class ContentAdmin(admin.ModelAdmin):
    list_display = ['title','type','image_tag','status','create_at']
    list_filter = ['status','type']
    inlines = [ContentImageInline]
    prepopulated_fields = {'slug':('title',)}
    def __str__(self):
        return self.title





class MenuAdmin(DraggableMPTTAdmin):
    mptt_indent_field = 'title'
    list_display = ['tree_actions','indented_title','status']
    list_filter = ['status']

    def __str__(self):
        return self.title

admin.site.register(Menu,MenuAdmin)
admin.site.register(Content,ContentAdmin)
