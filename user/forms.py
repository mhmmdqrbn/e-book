from django import forms
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import fields
from django.forms import widgets
from home.models import UserProfile
from django.contrib.auth.forms import UserChangeForm

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50,label="Istifadeci adi ", widget=forms.TextInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=50,label="Adınız ", widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=50,label="Soyadınlz ", widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(max_length=50,label="E-mail ", widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(max_length=20,label="Şifrə", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    confirm = forms.CharField(max_length=20,label='Təkrar Şifrə',widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        confirm = self.cleaned_data.get('confirm')

        if password and confirm and password != confirm:
            raise forms.ValidationError('Şifrə eyni deyil!')

        
        values ={
            'username':username,
            'password':password,
            'first_name':first_name,
            'last_name':last_name,
            'email':email,
            'confirm':confirm
        }
        return values


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = {'username','email','first_name','last_name'}
        widgets = {
            'username' : widgets.TextInput(attrs={'class':'input','placeholder':'username'}),
            'first_name' : widgets.TextInput(attrs={'class':'input','placeholder':'first_name'}),
            'email' : widgets.EmailInput(attrs={'class':'input','placeholder':'email'}),
            'last_name' : widgets.TextInput(attrs={'class':'input','placeholder':'last_name'})

        }

CITY = {
    ('Baki','Baki'),
    ('Qazax','Qazax'),
    ('Sumqayit','Sumqayit')
}

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone','address','city','country','image')
        widgets = {
            'phone' : widgets.TextInput(attrs={'class':'input','placeholder':'nömrə'}),
            'address' : widgets.TextInput(attrs={'class':'input','placeholder':'address'}),
            'city' : widgets.Select(attrs={'class':'input','placeholder':'şəhər'},choices=CITY),
            'country' : widgets.TextInput(attrs={'class':'input','placeholder':'ölkə'}),
            'image' : widgets.FileInput(attrs={'class':'input','placeholder':'şəkil'}),
        }




