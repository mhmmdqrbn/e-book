from django.db import models
from django.db.models import fields
from django.utils.safestring import mark_safe
from django.forms import ModelForm
from django.contrib.auth.models import User

from django.urls import reverse
from mptt.models import MPTTModel,TreeForeignKey
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.



class Category(MPTTModel):

    STATUS = (
        ('True','Beli'),
        ('False','Xeyr')
    )
    
    title = models.CharField(max_length=200)
    keywords = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    image = models.ImageField(blank = True,upload_to = "images/")
    status = models.CharField(max_length=10,choices=STATUS)
    slug = models.SlugField(unique=True,null=False)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


    class MPTTMeta:
        order_insertion_by = ['title']


    def __str__(self):
        full_path = [self.title ]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' -> '.join(full_path[::-1])
    def image_tag(self):
        return mark_safe('<img src ="{}" height = "50"'.format(self.image.url))
    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse('category_detail',kwargs = {'slug':self.slug})
    



class Product(models.Model):

    STATUS = (
        ('Var','Beli'),
        ('Yox','Xeyr')
    )
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=30)
    keywords = models.CharField(blank=True,max_length=255)
    description = models.CharField(blank=True,max_length=255)
    image = models.ImageField(blank = True, null=True, upload_to = 'images/',default='uploads/images/indir.jpg')
    price = models.FloatField()
    oldprice = models.FloatField()
    amount = models.IntegerField()
    detail = RichTextUploadingField()
    slug = models.SlugField(unique=True,null=False)
    status = models.CharField(max_length=10,choices=STATUS , default=True)
    favorite = models.ManyToManyField(User , related_name='favorite',blank=True , default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    product_view = models.PositiveIntegerField(default=0,blank=True,null=True)
    def __str__(self):
        return self.title
    

    def image_tag(self):
        return mark_safe('<img src ="{}" height = "50"'.format(self.image.url))
    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse('product_detail',kwargs = {'slug':self.slug})

class Images(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    title = models.CharField(max_length=50,blank = True)
    image = models.ImageField(blank = True, upload_to = 'images/')

    def __str__(self):
        return self.title
    def image_tag(self):
        return mark_safe('<img src ="{}" height = "50"'.format(self.image.url))
    image_tag.short_description = 'Image'



class Comment(models.Model):
    STATUS = (
        ('New','Yeni'),
        ('True','Beli'),
        ('False','Xeyr')
    )
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    comment = models.CharField(max_length=250,blank=True)
    rate = models.IntegerField(blank=True)
    status = models.CharField(max_length=10,choices=STATUS,default='New')
    ip = models.CharField(blank=True,max_length=20)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.subject
    

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields= ['subject','comment','rate']