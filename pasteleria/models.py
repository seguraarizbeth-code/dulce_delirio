# store/models.py
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

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
# 🥚 Ingrediente (NUEVA TABLA)
# =========================
class Ingredient(models.Model):
    """Ingredientes que pueden contener los productos de pastelería"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, verbose_name="Nombre del ingrediente")
    description = models.TextField(blank=True, verbose_name="Descripción")
    is_allergen = models.BooleanField(default=False, verbose_name="¿Es alérgeno común?")
    allergen_type = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name="Tipo de alérgeno",
        help_text="Ej: Gluten, Lácteos, Huevo, Frutos secos, etc."
    )
    
    class Meta:
        verbose_name_plural = "Ingredientes"
        ordering = ['name']
        
    def __str__(self):
        if self.is_allergen:
            return f"{self.name} ⚠️ ({self.allergen_type})"
        return self.name

# =========================
# 🧁 Producto (Pastel) - ACTUALIZADO
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
    
    # Campos de pastelería
    size = models.CharField(max_length=3, choices=SIZE_CHOICES, default='MD', verbose_name="Tamaño")
    flavor = models.CharField(max_length=100, verbose_name="Sabor")
    preparation_time = models.CharField(max_length=50, blank=True, verbose_name="Tiempo de preparación", help_text="Ej: 45 min, 2 horas")
    is_available = models.BooleanField(default=True, verbose_name="¿Disponible?")
    
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
    
    # 🆕 Relación ManyToMany: Un producto puede tener muchos ingredientes
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='products',
        verbose_name="Ingredientes",
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    class Meta:
        verbose_name_plural = "Productos"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.get_size_display()}) - {self.flavor}"
    
    @property
    def average_rating(self):
        """Calcula el promedio de calificaciones del producto"""
        reviews = self.reviews.all()
        if reviews.exists():
            return round(reviews.aggregate(models.Avg('rating'))['rating__avg'], 1)
        return 0
    
    @property
    def allergens(self):
        """Devuelve lista de ingredientes que son alérgenos"""
        return self.ingredients.filter(is_allergen=True)
    
    @property
    def is_in_stock(self):
        """Verifica si hay stock disponible"""
        return self.stock > 0 and self.is_available

# =========================
# ⭐ Reseña/Valoración (NUEVA TABLA)
# =========================
class Review(models.Model):
    """Reseñas y calificaciones de productos por parte de clientes"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='reviews',
        verbose_name="Producto"
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='reviews',
        verbose_name="Cliente"
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Calificación",
        help_text="Del 1 al 5"
    )
    comment = models.TextField(verbose_name="Comentario")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de reseña")
    
    class Meta:
        verbose_name_plural = "Reseñas"
        ordering = ['-created_at']
        # Un usuario solo puede dejar una reseña por producto
        unique_together = ['product', 'user']
    
    def __str__(self):
        return f"{'⭐' * self.rating} - {self.user.username} sobre {self.product.name}"

# =========================
# 🛒 Carrito (Sin cambios)
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
        return sum(item.subtotal for item in self.cartitem_set.all())

# =========================
# 📦 CartItem (Sin cambios)
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
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"