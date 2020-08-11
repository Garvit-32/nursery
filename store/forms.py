from django import forms
from django.contrib.auth.forms import UserCreationForm,PasswordResetForm
from django.contrib.auth.models import User
from .models import SellerAccount,Product
from django.conf import settings

class SignUpForm(UserCreationForm):
    username = forms.CharField(required=False)
    first_name = forms.CharField(max_length=70,required=True,widget=forms.TextInput(attrs={'type':"text",'placeholder':'','class':'form-control'}))
    last_name = forms.CharField(max_length=70,required=True,widget=forms.TextInput(attrs={'type':"text",'placeholder':'','class':'form-control'}))
    email = forms.EmailField(max_length=254,required=True,widget=forms.TextInput(attrs={'type':"email",'placeholder':'','class':'form-control'}))
    phone = forms.CharField(max_length=11,widget=forms.TextInput(attrs={'type':"text",'placeholder':'','class':'form-control'}))
    password1 = forms.CharField(min_length=8,strip=False,widget=forms.PasswordInput(attrs={'type':"password",'placeholder':'','class':'form-control'}))
    password2 = forms.CharField(min_length=8,strip=False,widget=forms.PasswordInput(attrs={'type':"password",'placeholder':'','class':'form-control'}))
    class Meta: 
        model = User
        fields = ('username','first_name','last_name',"phone",'email','password2','password1')

    def clean_first_name(self):
        _dict = super(SignUpForm,self).clean()
        return _dict['first_name'].capitalize()

    def clean_phone(self):
        _dict = super(SignUpForm,self).clean()
        if not _dict['phone'].isdigit():
            raise forms.ValidationError('Phone number invalid')
        _dict['phone'] = _dict['phone'][-10:]
        return _dict['phone']

    def clean_last_name(self):
        _dict = super(SignUpForm,self).clean()
        return _dict['last_name'].capitalize()

    def clean_email(self):
        if User.objects.filter(email__iexact=self.data['email']).exists():
            raise forms.ValidationError('This email is already registered')
        return self.data['email']
        

class SellerAccountForm(forms.ModelForm):
    class Meta:
        model = SellerAccount
        fields = ['sellerId','name',"email","phone","organization"]

    def clean_name(self):
        _dict = super(SellerAccountForm,self).clean()
        return _dict['name'].capitalize()

    def clean_phone(self):
        _dict = super(SellerAccountForm,self).clean()
        if not _dict['phone'].isdigit():
            raise forms.ValidationError('Phone number invalid')
        _dict['phone'] = _dict['phone'][-10:]
        return _dict['phone']
        
    def clean_organization(self):
        _dict = super(SellerAccountForm,self).clean()
        return _dict['organization'].capitalize()


class addPlantForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['sellerId','name',"price","desc","image"]


    