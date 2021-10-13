from django.urls import reverse
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.utils.safestring import mark_safe

# Create your models here.

class Menu(MPTTModel):
    STATUS = (
        ('True','Beli'),
        ('False','Xeyr')
    )
    parent = TreeForeignKey('self', blank = True, null = True , related_name='children',on_delete=models.CASCADE)
    title = models.CharField(max_length=180,unique=True)
    link = models.CharField(max_length=180,blank = True)
    status = models.CharField(max_length=180,choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    class MPTTMeta:
        order_insertion_by = ['title']


    def __Str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return '/'.join(full_path[::-1])


class Content(models.Model):
    Type = (
        ('xəbər','xəbər'),
        ('bildirim','bildirim'),
        ('endirim','endirim')
    )

    STATUS = (
        ('True','Beli'),
        ('False','Xeyr')
    )

    menu = models.OneToOneField(Menu,null=True,blank=True,on_delete=models.CASCADE)
    type = models.CharField(max_length=10,choices=Type)
    title = models.CharField(max_length=150)
    keywords = models.CharField(blank=True,max_length=255)
    description = models.CharField(blank=True,max_length=255)
    image = models.ImageField(blank=True,upload_to ='images/',default='uploads/images/indir.jpg')
    detail = models.CharField(null=False,max_length=255)
    slug = models.SlugField(blank=True,max_length=255)
    status = models.CharField(max_length=15,choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height = "35"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse("content_detail", kwargs={"slug": self.slug})
    

class CImages(models.Model):
    content = models.ForeignKey(Content,on_delete=models.CASCADE)
    title = models.CharField(max_length=50,blank=True)
    image = models.ImageField(blank=True , upload_to = 'images/')
    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height = "50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'