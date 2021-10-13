from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from product.models import Category, Product
# Create your models here.

class CreateProductModel(models.Model):
    product = models.OneToOneField(Product,on_delete=models.CASCADE)
    category = models.OneToOneField(Category,on_delete=models.CASCADE)
    title = models.CharField(blank=True,max_length=20)
    author = models.CharField(blank=True,max_length=150)
    description = models.CharField(blank=True,max_length=20)
    price = models.FloatField()
    amount = models.IntegerField()
    slug = models.SlugField(unique=True,null=False)
    detail = RichTextUploadingField()
    status = models.CharField(max_length=10)
    image = models.ImageField(blank=True,upload_to='uploads/',default='uploads/images/indir.jpg' )

    def __str__(self):
        return self.title
