from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Product, Review

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
        fields = [
            'name', 'description', 'image', 'price', 'stock', 
            'size', 'flavor', 'preparation_time', 'is_available',
            'categories', 'ingredients'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'categories': forms.CheckboxSelectMultiple(),
            'ingredients': forms.CheckboxSelectMultiple(),  # Selector múltiple para ingredientes
        }
        labels = {
            'name': 'Nombre del Pastel',
            'description': 'Descripción',
            'image': 'Fotografía',
            'price': 'Precio (MXN)',
            'stock': 'Existencia',
            'size': 'Tamaño',
            'flavor': 'Sabor',
            'preparation_time': 'Tiempo de preparación',
            'is_available': '¿Producto disponible?',
            'categories': 'Categorías',
            'ingredients': 'Ingredientes',
        }

class ReviewForm(forms.ModelForm):
    """Formulario para crear reseñas"""
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[
                (1, '⭐ - Malo'),
                (2, '⭐⭐ - Regular'),
                (3, '⭐⭐⭐ - Bueno'),
                (4, '⭐⭐⭐⭐ - Muy bueno'),
                (5, '⭐⭐⭐⭐⭐ - Excelente'),
            ]),
            'comment': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': 'Cuéntanos tu experiencia con este producto...'
            }),
        }
        labels = {
            'rating': 'Tu calificación',
            'comment': 'Tu comentario',
        }
