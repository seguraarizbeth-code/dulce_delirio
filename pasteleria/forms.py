# store/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Product

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico")
    is_seller = forms.BooleanField(required=False, label="Registrarse como vendedor")

    class Meta:
        model = User
        fields = ('username', 'email', 'is_seller', 'password1', 'password2')
        labels = {
            'username': 'Nombre de usuario',
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'price', 'stock', 'size', 'flavor', 'categories']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'categories': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'name': 'Nombre del Pastel',
            'description': 'Descripción',
            'image': 'Fotografía',
            'price': 'Precio (MXN)',
            'stock': 'Existencia',
            'size': 'Tamaño',
            'flavor': 'Sabor',
            'categories': 'Categorías',
        }