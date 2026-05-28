from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Product, Review, Order

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
# =========================
# Formulario de Pago (NUEVO)
# =========================
class PaymentForm(forms.Form):
    payment_method = forms.ChoiceField(
        choices=Order.PAYMENT_METHODS,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Método de pago"
    )
    
    # Campos para tarjeta (solo se muestran condicionalmente)
    card_holder_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Como aparece en la tarjeta'}),
        label="Nombre del titular"
    )
    card_number = forms.CharField(
        max_length=19,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234 5678 9012 3456'}),
        label="Número de tarjeta"
    )
    card_expiry = forms.CharField(
        max_length=5,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/AA'}),
        label="Fecha de expiración"
    )
    card_cvv = forms.CharField(
        max_length=4,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '123'}),
        label="CVV"
    )
    
    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get('payment_method')
        
        if payment_method == 'CARD':
            required_fields = ['card_holder_name', 'card_number', 'card_expiry', 'card_cvv']
            for field in required_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, 'Este campo es obligatorio para pagos con tarjeta.')
        
        # Validación simple de tarjeta (solo formato)
        if payment_method == 'CARD' and cleaned_data.get('card_number'):
            import re
            card_num = re.sub(r'\D', '', cleaned_data['card_number'])
            if len(card_num) < 13 or len(card_num) > 19:
                self.add_error('card_number', 'Número de tarjeta inválido (debe tener entre 13 y 19 dígitos).')
        
        return cleaned_data