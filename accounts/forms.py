from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class OrderForm(ModelForm):
    # error_css_class = 'error'
    # use_required_attribute = 'required'

    class Meta:
        model = Order
        fields = "__all__"


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude =['user']

