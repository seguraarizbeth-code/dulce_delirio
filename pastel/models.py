# pasteleria/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# ============================================
# MODELO DE USUARIO PERSONALIZADO
# ============================================
class Usuario(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    es_pastelero = models.BooleanField(default=False)  # Para vendedores/pasteleros
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.username


# ============================================
# CATEGORÍAS DE PASTELES
# ============================================
class Categoria(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    slug = models.SlugField(unique=True, max_length=120)
    imagen_icono = models.ImageField(upload_to='categorias/', blank=True, null=True)
    
    class Meta:
        verbose_name_plural = 'Categorías'
        ordering = ('nombre',)
    
    def __str__(self):
        return self.nombre


# ============================================
# PRODUCTOS (PASTELES)
# ============================================
class Producto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    nombre = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=280)
    descripcion_corta = models.CharField(max_length=255, blank=True)
    descripcion_larga = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    imagen_secundaria = models.ImageField(upload_to='productos/', blank=True, null=True)
    
    # Toque creativo - Sabores y personalización
    sabor_base = models.CharField(max_length=100, blank=True, null=True)  # Vainilla, Chocolate, etc.
    relleno = models.CharField(max_length=100, blank=True, null=True)  # Dulce de leche, Frutas, etc.
    peso_kg = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    es_personalizable = models.BooleanField(default=True)
    esta_activo = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Estados para el producto
    ACTIVO = 'activo'
    AGOTADO = 'agotado'
    OCULTO = 'oculto'
    
    CHOICES_ESTADO = [
        (ACTIVO, 'Activo'),
        (AGOTADO, 'Agotado'),
        (OCULTO, 'Oculto'),
    ]
    
    estado = models.CharField(max_length=10, choices=CHOICES_ESTADO, default=ACTIVO)
    
    def __str__(self):
        return self.nombre
    
    def get_absolute_url(self):
        return f'/pastel/{self.slug}/'


# ============================================
# CARRITO DE COMPRAS
# ============================================
class Carrito(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='carritos')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    ESTADO_ACTIVO = 'activo'
    ESTADO_ABANDONADO = 'abandonado'
    ESTADO_CONVERTIDO = 'convertido'
    
    CHOICES_ESTADO = [
        (ESTADO_ACTIVO, 'Activo'),
        (ESTADO_ABANDONADO, 'Abandonado'),
        (ESTADO_CONVERTIDO, 'Convertido'),
    ]
    
    estado = models.CharField(max_length=15, choices=CHOICES_ESTADO, default=ESTADO_ACTIVO)
    
    def __str__(self):
        return f"Carrito de {self.usuario.username}"
    
    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())


# ============================================
# ITEMS DEL CARRITO (con personalización)
# ============================================
class ItemCarrito(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    
    # ✨ TOQUE CREATIVO - Personalización del pastel
    mensaje_dedicatoria = models.TextField(blank=True, null=True)  # "Feliz Cumpleaños Mamá"
    decoracion_extra = models.CharField(max_length=255, blank=True, null=True)  # "Chispas doradas"
    color_masa = models.CharField(max_length=50, blank=True, null=True)  # Rosa, Azul, Verde
    sabor_personalizado = models.CharField(max_length=100, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('carrito', 'producto')
    
    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
    
    @property
    def subtotal(self):
        return self.producto.precio * self.cantidad


# ============================================
# PEDIDOS (Con sistema de calendario)
# ============================================
class Pedido(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    numero_pedido = models.CharField(max_length=20, unique=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='pedidos')
    
    # Fechas importantes para el sistema de calendario
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    fecha_entrega_solicitada = models.DateField()  # 🔥 CLAVE PARA CALENDARIO
    
    # Flujo de producción (como en tu proyecto)
    fecha_horneado = models.DateTimeField(blank=True, null=True)  # "En horno"
    fecha_listo = models.DateTimeField(blank=True, null=True)     # "Listo"
    fecha_entregado = models.DateTimeField(blank=True, null=True) # "Entregado"
    
    # Estados del pedido
    PENDIENTE = 'pendiente'
    EN_HORNO = 'en_horno'
    LISTO = 'listo'
    ENTREGADO = 'entregado'
    CANCELADO = 'cancelado'
    
    CHOICES_ESTADO = [
        (PENDIENTE, 'Pendiente'),
        (EN_HORNO, 'En horno 🎂'),
        (LISTO, 'Listo para entregar ✨'),
        (ENTREGADO, 'Entregado ✅'),
        (CANCELADO, 'Cancelado ❌'),
    ]
    
    estado = models.CharField(max_length=15, choices=CHOICES_ESTADO, default=PENDIENTE)
    
    # Datos financieros
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    impuesto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Datos de entrega
    direccion_entrega = models.TextField()
    telefono_contacto = models.CharField(max_length=20, blank=True)
    notas_adicionales = models.TextField(blank=True)
    metodo_pago = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return f"{self.numero_pedido} - {self.usuario.username}"
    
    class Meta:
        ordering = ('-fecha_pedido',)
        indexes = [
            models.Index(fields=['fecha_entrega_solicitada']),  # Para calendario rápido
            models.Index(fields=['estado']),
        ]


# ============================================
# DETALLES DEL PEDIDO (Snapshot de compra)
# ============================================
class DetallePedido(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    
    # Snapshot de datos (se guardan en el momento de la compra)
    nombre_producto = models.CharField(max_length=255)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    
    # ✨ TOQUE CREATIVO - Guardamos la personalización del pedido
    mensaje_dedicatoria = models.TextField(blank=True, null=True)
    sabor_seleccionado = models.CharField(max_length=100, blank=True, null=True)
    decoracion_especial = models.CharField(max_length=255, blank=True, null=True)
    url_imagen_referencia = models.URLField(blank=True, null=True)  # Cliente sube diseño
    
    def __str__(self):
        return f"{self.cantidad} x {self.nombre_producto}"
    
    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario