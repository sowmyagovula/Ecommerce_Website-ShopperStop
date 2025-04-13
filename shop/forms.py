from django import forms
from .models import Shop_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProductForm(forms.ModelForm):
    class Meta:
        model = Shop_model
        fields = ['category', 'brand', 'product_name', 'price', 'desc', 'image']

USER_TYPE_CHOICES = (
    ('buyer', 'Buyer'),
    ('seller', 'Seller'),
)

class UserRegistrationForm(UserCreationForm):
    
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ('username', 'email', 'user_type', 'password1', 'password2')