from ckeditor import fields
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.base import Model
from django.forms import ModelForm
from django.forms.widgets import TextInput, Textarea
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

# Create your models here.


class Setting(models.Model):
    STATUS = (
        ('True','Beli'),
        ('False','Xeyr')
    )

    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    company = models.CharField(max_length=50)
    address = models.CharField(blank = True ,max_length=150)
    phone = models.CharField(blank = True ,max_length=15)
    fax = models.CharField(blank = True ,max_length=50)
    email = models.CharField(blank = True ,max_length=30)
    smtpserver = models.CharField(blank = True ,max_length=30)
    smtpemail = models.CharField(blank = True ,max_length=30)
    smtppassword = models.CharField(blank = True ,max_length=30)
    smtpport = models.CharField(blank = True ,max_length=5)
    icon = models.ImageField(blank = True , upload_to ='images/')
    facebook = models.CharField(blank = True ,max_length=50)
    instagram = models.CharField(blank = True ,max_length=50)
    twitter = models.CharField(blank = True ,max_length=50)
    aboutus = RichTextUploadingField(blank = True )
    contact = RichTextUploadingField(blank = True )
    references = RichTextUploadingField(blank = True)
    status = models.CharField(max_length=30,choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title



class ContactFormMessage(models.Model):
    STATUS = (
        ('New','Yeni'),
        ('Read','Oxunub')
    )
    name = models.CharField(blank=True,max_length=30)
    email = models.CharField(blank=True,max_length=30)
    subject = models.CharField(blank=True,max_length=50)
    message = models.CharField(blank=True,max_length=250)
    status = models.CharField(max_length=10,choices=STATUS,default='Yeni')
    note = models.CharField(blank=True,max_length=250)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ContactForm(ModelForm):
    class Meta:
        model = ContactFormMessage
        fields=['name','email','subject','message']
        widgets = {
            'name': TextInput(attrs={'class' : 'input','placeholder':'Ad və Soyad'}),
            'subject': TextInput(attrs={'class' : 'input','placeholder':'Başlıq'}),
            'email': TextInput(attrs={'class' : 'input','placeholder':'Email'}),
            'message': Textarea(attrs={'class' : 'input','placeholder':'Mesajınız'})

        }

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(blank=True,max_length=20)
    address = models.CharField(blank=True,max_length=150)
    city = models.CharField(blank=True,max_length=20)
    country = models.CharField(blank=True,max_length=20)
    image = models.ImageField(blank=True,upload_to='images/users/')

    def __str__(self):
        return self.user.username 


    def user_name(self):
        return self.user.username


    def image_tag(self):
        return mark_safe('<img src ="{}" height = "25"'.format(self.image.url))
    image_tag.short_description = 'Image'

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = {'phone','address','city','country','image'}



class FAQ(models.Model):
    STATUS = (
        ('True','True'),
        ('False','False')
    )

    ordernumber = models.IntegerField()
    question = models.CharField(max_length=150)
    answer = models.TextField()
    status = models.CharField(max_length=10,choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return self.question