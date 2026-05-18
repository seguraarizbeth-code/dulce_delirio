# store/models.py
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# =========================
# 👤 Usuario
# =========================
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_seller = models.BooleanField(default=False, verbose_name="¿Es vendedor?")

    def __str__(self):
        return self.username

# =========================
# 🏷️ Categoría
# =========================
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name="Nombre")
    description = models.TextField(blank=True, verbose_name="Descripción")

    class Meta:
        verbose_name_plural = "Categorías"
        
    def __str__(self):
        return self.name

# =========================
# 🧁 Producto (Pastel)
# =========================
class Product(models.Model):
    SIZE_CHOICES = [
        ('CH', 'Chico'),
        ('MD', 'Mediano'),
        ('GD', 'Grande'),
        ('XXL', 'Extragrande'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, verbose_name="Nombre del producto")
    description = models.TextField(verbose_name="Descripción")
    image = models.ImageField(upload_to='upload/', blank=True, null=True, verbose_name="Imagen")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    stock = models.PositiveIntegerField(default=0, verbose_name="Existencia")
    
    # Nuevos campos para la pastelería
    size = models.CharField(max_length=3, choices=SIZE_CHOICES, default='MD', verbose_name="Tamaño")
    flavor = models.CharField(max_length=100, verbose_name="Sabor")
    
    # Relación OneToMany: Un vendedor puede tener muchos productos
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Vendedor"
    )

    # Relación ManyToMany: Un producto puede estar en muchas categorías
    categories = models.ManyToManyField(
        Category,
        related_name='products',
        verbose_name="Categorías"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        verbose_name_plural = "Productos"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.get_size_display()}) - {self.flavor}"

# =========================
# 🛒 Carrito
# =========================
class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name="Usuario"
    )
    products = models.ManyToManyField(
        Product,
        through='CartItem',
        related_name='carts'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    def __str__(self):
        return f"Carrito de {self.user.username}"

    @property
    def total(self):
        """Calcula el total del carrito."""
        return sum(item.subtotal for item in self.cartitem_set.all())

# =========================
# 📦 CartItem (Producto en el carrito)
# =========================
class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name="Carrito")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Producto")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Cantidad")

    class Meta:
        unique_together = ('cart', 'product')
        verbose_name = "Artículo del carrito"
        verbose_name_plural = "Artículos del carrito"

    @property
    def subtotal(self):
        """Calcula el subtotal de este artículo."""
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} en carrito de {self.cart.user.username}"