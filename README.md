==========ÍNDICE==========

'INTRODUCCIÓN' ........................................................ 3


'DESARROLLO' .......................................................... 5


'TIPO DE RELACIONES' .................................................. 13


'DISEÑO DE LA BASE DE DATOS' .......................................... 16


'ADMINISTRACIÓN DEL SISTEMA' .......................................... 17


'ELIMINACIÓN DE DATOS' ................................................ 19


'ACTUALIZACIÓN DE DATOS' .............................................. 20


'FUNCIONAMIENTO DE LOS VIEWS Y SUS INTERACCIONES' ..................... 21


'VIEWS Y URLS' ........................................................ 21


'VIEWS Y TEMPLATES' ................................................... 21


'INTEGRACIÓN DEL SISTEMA' ............................................. 21


'CONCLUSIONES FINALES' ................................................ 23







==========INTRODUCCIÓN==========

El objetivo de este documento fue ir recalcando puntos importantes sobre este último parcial en la que teníamos que realizar un proyecto con, lo que ya habíamos visto anteriormente, lo cual decidimos hacer sobre una pastelería, que básicamente podría parecerse a una tienda online en la que utilizamos varios modelos para que pudiera guardar la información acerca de los clientes, precios, actividades del admin entre otras cosas.

Este proyecto tiene como objetivo aplicar la relación que tiene Python de uno a uno, uno a muchos y muchos a muchos, para demostrar el aprendizaje y rendimiento que tuvimos en esta materia a lo largo del semestre, al igual que aplicar lo visto en clases pasadas. Uno de los objetivos principales es comercializar y promocionar distintos postres de manera online, para satisfacer los antojos de los clientes y facilitar su pedido. 

El propósito es mostrar a los clientes la autenticidad y sabor tan único de los postres, al igual que la originalidad de una pastelería en línea.

Nuestro proyecto está basado en vender productos de calidad en la que los clientes pueden pedir, dejar ordenes para fechas importantes y obtener precios accesibles,también contamos con los ingredientes que tu quisieras que tengan tus pasteles y recomendaciones o críticas que pudieron mejorar la pastelería,tiene acceso al carrito para ordenar y tiene para que puedas decidir la forma en la que puedes pagar,tienes acceso de las fechas en las que estuvieron disponibles los productos y a que hora los subieron para poder comparar en momentos exactos.

Además, el proyecto fue desarrollado pensando en que fuera fácil de usar tanto para los clientes como para el administrador de la página.
Por eso se implementaron diferentes funciones que ayudan a organizar mejor la información y mantener un control sobre los productos y pedidos realizados.

Dentro de la aplicación también se pueden registrar datos importantes de los usuarios, como sus pedidos, productos seleccionados y métodos de pago, permitiendo que la información quede almacenada en la base de datos. De igual manera, el admin puede agregar, modificar, visualizar y eliminar información desde el panel de administración.

Para el desarrollo del proyecto se utilizaron modelos relacionados entre sí, lo que permitió conectar la información de manera más organizada. Gracias a esto, los productos pueden relacionarse con categorías, pedidos y clientes dentro de la plataforma.

También se trabajó en la parte visual de la aplicación para que la página tuviera una apariencia más ordenada y llamativa para los usuarios. Se buscó que la navegación fuera sencilla y que los clientes pudieran encontrar fácilmente los productos y opciones disponibles dentro de la pastelería en línea.
Este proyecto ayudó a reforzar nuestros conocimientos sobre programación, bases de datos relacionales y desarrollo web, poniendo en práctica diferentes herramientas vistas durante el semestre.




| Tecnología / Herramienta | Uso dentro del proyecto |
| :--- | :--- |
| `Python` | Lenguaje de programación principal utilizado para desarrollar toda la lógica del sistema y el funcionamiento del backend. |
| `Django 5.2` | Framework utilizado para crear la aplicación web, administrar modelos, views, urls, formularios y el panel administrativo. |
| `Visual Studio Code` | Editor de código utilizado para programar, organizar y ejecutar el proyecto de manera eficiente. |
| `GitHub` | Plataforma utilizada para almacenar el repositorio del proyecto, guardar avances y realizar control de versiones del código. |
| `HTML` | Lenguaje utilizado para crear la estructura visual de las páginas web del sistema. |
| `CSS` | Utilizado para diseñar y dar estilos visuales a la interfaz de la pastelería. |
| `Bootstrap` | Framework de diseño utilizado para crear interfaces más modernas, organizadas y adaptables. |
| `SQLite` | Base de datos utilizada para almacenar información de usuarios, productos, pedidos, reseñas y pagos. |





==========DESARROLLO==========



--------Modelos-------

Se utilizaron diferentes modelos dentro de la base de datos, los cuales permiten guardar y organizar la información de manera más sencilla. Cada modelo tiene su función en el sistema, como usuarios, productos, categorías, ingredientes, reseñas, etc. Todos ayudan a que la información se conecte y que así el programa funcione correctamente.



--------Modelo “User”--------

class User(AbstractUser):
Se utiliza para guardar la información de los usuarios que se registren en la página. Se agregó una opción para saber si el usuario es cliente o admin, también incluye datos básicos, como el nombre de usuario, contraseña y correo electrónico.



-------Modelo “Category”-------

class Category(models.Model):
Se utiliza para guardar las categorías de los productos de la pastelería, cada una tiene un nombre y descripción para organizar los postres dentro de la página. De esta manera se encuentran de manera más eficaz y sencilla dependiendo de lo que el cliente esté buscando. 



--------Modelo “Ingredient”-------

class Ingredient(models.Model):
Este modelo es para almacenar los ingredientes que se utilizan en la papelería, que nos deja registrar y organizar la información de cada uno, para saber qué contiene cada uno.
este campo indica si puede tener algún tipo de halogeno para que los clientes puedan saber lo que contiene cada pastel y saber si son alérgicos a algún ingrediente.

allergen_type = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Tipo de alérgeno",
        help_text="Ej: Gluten, Lácteos, Huevo, Frutos secos, etc."


--------Modelo “Product”--------

class Product(models.Model):
Este es principal en el proyecto, guarda toda la información relacionada con los productos de la pastelería, como:

Nombre del producto 
name = models.CharField(max_length=150, verbose_name="Nombre del producto")

descripción
description = models.TextField(verbose_name="Descripción")

imagen 
image = models.ImageField(upload_to='upload/', blank=True, null=True, verbose_name="Imagen")

precio
price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")

cantidad
stock = models.PositiveIntegerField(default=0, verbose_name="Existencia")

tamaño
size = models.CharField(max_length=3, choices=SIZE_CHOICES, default='MD', verbose_name="Tamaño")

sabor
flavor = models.CharField(max_length=100, verbose_name="Sabor")



-------Modelo “Review”-------

class Review(models.Model):
Se utiliza para guardar reseñas que hacen los clientes sobre los productos, cada reseña incluye:

Producto relacionado
product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Producto"

Usuario que hizo la reseña
 user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Cliente"

Calificación del 1-5
rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Calificación",
        help_text="Del 1 al 5"

Comentario que se hizo 
  comment = models.TextField(verbose_name="Comentario")
Fecha en que se hizo 
created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de reseña")


-------Modelos “Cart”--------

Permite guardar los productos que el cliente quiere comprar antes de terminar el pedido, además de calcular el total de tu compra según la cantidad de productos que hayas agregado.
class Cart(models.Model):


-------Modelo “Cartltem”--------

class CartItem(models.Model):
Se utiliza para relacionar los productos del carrito de compras, también calcula el total dependiendo la cantidad de productos y su precio, por eso es que el carrito puede tener varios productos al mismo tiempo en una sola compra. El modelo guarda:

El carrito relacionado
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name="Carrito")

El producto agregado
    quantity = models.PositiveIntegerField(default=1, verbose_name="Cantidad")

La cantidad seleccionada
    quantity = models.PositiveIntegerField(default=1, verbose_name="Cantidad")



==========Views==========

Fueron utilizados para la lógica y funcionamiento de la página, se encargan de conectar la base de datos con las plantillas para mostrar la información correcta al usuario. Con estas se pueden controlar funciones como el registro de usuario e inicio de sesión, administrar productos, carrito de compras, reseñas, etc.


--------Vista “Home”--------

def home(request):
Funciona como página principal de la pastelería, se muestran los productos disponibles junto con distintos filtro y un buscador, también se agregaron páginas para mostrar los productos de forma más organizada, mostrando cierta cantidad por página. Los usuarios pueden buscar:

Nombre
 if query:
        products = products.filter(
            Q(name__icontains=query)

Descripción
 if query:
        products = products.filter(
            Q(description__icontains=query)

Sabor
 if flavor_query:
        products = products.filter(flavor__icontains=flavor_query)

Categoría
 if category_id:
        products = products.filter(categories__id=category_id)

Tamaño
if size_filter:
        products = products.filter(size=size_filter)

Ingredientes 
if ingredient_filter:
        products = products.filter(ingredients__id=ingredient_filter)



-------Vista “Register”--------

Se utiliza para registrar nuevos usuarios dentro de la página, si hace los pasos correctos el usuario se guarda automáticamente en la base de datos y después puede iniciar sesión dentro de la página
def register(request)


--------Vista ”Login_view”-------

Permite que los usuarios inicien sesión utilizando el nombre de usuario y contraseña. Si los datos son correctos el sistema va a mandarlo al sitio correspondiente dependiendo si es cliente o administrador
def login_view(request)
Vista “Logout_view”
Es para cerrar la sesión del usuario actual en la página y regresar al inicio de la página 
def logout_view(request)


--------Vista “Dashboard”--------

def dashboard(request):
Funciona como panel de administración para los vendedores/administradores, además de verificar que solo los vendedores/administradores tengan acceso a esta parte del sistema, tales como:

Sus productos
    products = Product.objects.filter(owner=request.user).prefetch_related('reviews', 'ingredients')

Total de productos registrados
    total_products = products.count()

Cantidad de reseñas
    total_reviews = Review.objects.filter(product__owner=request.user).count()

Promedio de calificaciones 
avg_rating = Review.objects.filter(product__owner=request.user).aggregate(
        avg=Avg('rating')
    )['avg'] or 0



--------Vista “Product_create”--------

def product_create(request):
Permite agregar nuevos productos a la base de datos, cuando se guarda correctamente el sistema manda un mensaje de confirmación. La información que puede registrarse es:

Nombre

Precio

Imagen

Sabor

Ingredientes

Tamaño

Existencia 


--------Vista “Product_update”--------

Se utiliza para modificar productos que ya están registrados, se verifica que el producto sea del vendedor que intenta editarlo para evitar cambios no autorizados.
def product_update(request, pk)


--------Vista “Product_delete”--------

Permite eliminar productos ya registrados en el sistema, antes de eliminar algún producto se manda solicitud de confirmación para evitar eliminaciones accidentales.
def product_delete(request, pk)


--------Vista “Product_detail”--------

def product_detail(request, pk):
Muestra toda la información detallada del producto, también permite que los usuarios registrados puedan dejar algún comentario o reseña sobre el producto. Cosas como:

Ingredientes

Reseñas

Calificaciones

Productos relacionados 


--------Vista “Cart_detail”--------

Muestra todos los productos agregados al carrito del usuario, se ven todos los productos seleccionados, cantidades y el total de la compra
def cart_detail(request):


--------Vista “Add_to_cart”--------

Se utiliza para agregar productos al carrito de compras, también verifica que el producto tenga existencia disponible antes de agregarlo.
def add_to_cart(request, product_id)


--------Vista “Remove_from_cart”--------

Permite eliminar productos del carrito de compras de usuarios 
def remove_from_cart(request, item_id)


--------Vista” Update_cart_item”--------

Se utiliza para modificar la cantidad de productos dentro del carrito. El sistema también verifica que no se agreguen más productos de los que ya existen.
def update_cart_item(request, item_id)

 
--------Vista “Checkout”--------

Se utiliza para ver la forma de realizar el pago de cada cliente,si va a hacer en efectivo,transferencia o pago con tarjeta de crédito,dentro de esa función te pide el nombre,el número de tarjeta y el número en el que vence la tarjeta para que no haya errores.


--------Vista "metodo de pago"--------

art, created = Cart.objects.get_or_create(user=request.user)
verificación si el carrito no está vacío
 if not cart.cartitem_set.exists():

Datos para registrar el pago
card_holder = form.cleaned_data.get('card_holder_name') if payment_method == 'CARD' else None

Guardar los dígitos del pedido
if card_last_digits:
crear registro de pago
este es uno de la linea de codigos para que sea funciona la forma de pagar.
 Payment.objects.create
response_message="Pago simulado exitoso"
 
vaciar carrito
para verificar que ya se realizo tu compra y puedes seguir  nuevamente comprando después de hacer realizar tu pago.
cart.cartitem_set.all().delete()
messages.success(request, f"¡Compra realizada con éxito! Tu pedido #{order.id} ha sido confirmado.")
def order_confirmation(request, order_id):


--------vista "confirmación de pedido"--------

def order_confirmation(request, order_id):
función para saber que compraste en la pastelería,cuanto fue por cada uno y el total.




===========Urls==========

Son los encargados de que cada enlace dentro de la página lleve a cabo la función correcta, y que muestra la información adecuada al usuario dependiendo de la acción que haga. Están organizados de manera que sustentan las funciones principales del sistema.


--------Página principal--------

Dirige a la persona a la página principal, del proyecto, donde muestra los productos que están disponibles con los filtros y buscador.
    path('', views.home, name='home')


--------Registro de usuarios--------

Permite que nuevos usuarios puedan crear una cuenta desde la plataforma 
    path('register/', views.register, name='register')


--------Inicio de sesión--------

Se utiliza para que los usuarios puedan iniciar sesión con su cuenta registrada
    path('login/', views.login_view, name='login')


--------Cierre de sesión--------

Permite cerrar la sesión del usuario actual y regresa a la página principal
    path('logout/', views.logout_view, name='logout')


--------Dashboard--------

Dirige al panel de administración a los vendedores, donde se pueden manipular los productos y ver estadísticas generales de estos 
    path('dashboard/', views.dashboard, name='dashboard'),


--------Crear productos--------

Permite registrar nuevos productos dentro de la pastelería 
    path('products/create/', views.product_create, name='product_create')

--------Editar productos--------

Permite modificar la información de un producto ya registrado en el sistema
    path('products/<uuid:pk>/edit/', views.product_update, name='product_update')


--------Eliminar productos--------

Se utiliza para eliminar productos del sistema 
    path('products/<uuid:pk>/delete/', views.product_delete, name='product_delete')


--------Detalle de productos-------- 

Muestra toda la información detallada de un producto, incluyendo reseñas, ingredientes y productos relacionados
    path('products/<uuid:pk>/', views.product_detail, name='product_detail')


--------Carrito de compras--------

Permite visualizar el contenido del carrito del usuario 
    path('cart/', views.cart_detail, name='cart_detail')


--------Agregar al carrito--------

Agrega un producto seleccionado al carrito de compras 
    path('cart/add/<uuid:product_id>/', views.add_to_cart, name='add_to_cart')


--------Eliminar del carrito--------

Permite eliminar un producto específico del carrito 
    path('cart/remove/<uuid:item_id>/', views.remove_from_cart, name='remove_from_cart')


--------Actualizar carrito--------

Se utiliza para cambiar la cantidad de un producto dentro del carrito de compras 
    path('cart/update/<uuid:item_id>/', views.update_cart_item, name='update_cart_item')

--------Forma de pago--------

se utiliza para saber de que forma va a pagar el cliente,en efectivo,con tarjeta ontransferencia.
 path('checkout/', views.checkout, name='checkout'),
path('order/<uuid:order_id>/', views.order_confirmation, name='order_confirmation')




**********TIPO DE RELACIONES**********

Dentro del proyecto se utilizaron distintos tipos de relaciones entre los modelos para lograr que la información del sistema se conecte correctamente, estas relaciones ayudan a organizar los datos de manera más eficaz y estructurada. Permiten que funciones como productos, reseñas, ingredientes y carrito de compras puedan actuar entre sí, dentro del programa.


--------USER-PRODUCTO--------

RELACIÓN UNO A MUCHOS

owner = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name='products',
    verbose_name="Vendedor"
)


--------USER - REVIEW--------

RELACIÓN UNO A MUCHOS

class Review(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Cliente"
    )



--------USER - ORDER --------

RELACIÓN UNO A MUCHOS

class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name="Cliente"
    )


--------PRODUCT - REVIEW--------

RELACIÓN UNO A MUCHOS

class Review(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Producto"
    )



--------CART - CARTLTEM--------

RELACIÓN UNO A MUCHOS

class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        verbose_name="Carrito"
    )



--------ORDER - ORDERLTEM--------

RELACIÓN UNO A MUCHOS
 
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Pedido"
    )


Este tipo de relación se utiliza cuando un registro puede estar relacionado con varios registros de otra tabla, pero esos registros sólo pertenecen a uno específico. 
En el proyecto se puede observar esta relación entre usuarios y reseñas, ya que un usuario puede realizar varias reseñas dentro de la página, pero cada reseña pertenece a un usuario. También se utiliza entre productos y reseñas, debido a que un producto puede tener varias opiniones hechas por distintos clientes.


--------PRODUCT - CATEGORY--------

RELACIÓN MUCHOS A MUCHOS

class Product(models.Model):
    # Relación ManyToMany: Un producto puede estar en muchas categorías
    categories = models.ManyToManyField(
        Category,
        related_name='products',
        verbose_name="Categorías"
    )

--------PRODUCT - INGREDIENT--------

RELACIÓN MUCHOS A MUCHOS 
class Product(models.Model):
    # Relación ManyToMany: Un producto puede tener muchos ingredientes
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='products',
        verbose_name="Ingredientes",
        blank=True
    )

Esta relación se utiliza cuando varios registros pueden relacionarse entre sí al mismo tiempo.
Dentro del proyecto se implementa entre productos e ingredientes, ya que un producto puede contener varios ingredientes y un mismo ingrediente puede utilizarse en distintos productos de la pastelería. Gracias a esto, la información se organiza de una manera más flexible y se evita repetir datos innecesarios dentro de la base de datos.
Relación uno a uno La relación uno a uno se utiliza cuando un registro solamente puede estar relacionado con otro único registro.




==========DISEÑO DE LA BASE DE DATOS==========

La base de datos del proyecto fue diseñada utilizando un modelo relacional, permitiendo organizar toda la información de manera estructurada y conectada entre sí. Este tipo de diseño ayuda a que los datos se almacenen de forma más ordenada dentro del sistema, facilitando el manejo de la información y evitando que existan datos repetidos o desorganizados.

Dentro del proyecto se utilizaron diferentes modelos que representan las partes principales del funcionamiento de la pastelería. Entre ellos se encuentran usuarios, productos, categorías, ingredientes, reseñas y carrito de compras. Cada uno cumple una función específica dentro del sistema y permite que la aplicación funcione correctamente tanto para los clientes como para los administradores.

Cada modelo contiene distintos campos que almacenan información importante. Por ejemplo, el modelo de productos guarda datos como el nombre, descripción, precio, imagen, sabor, tamaño y cantidad disponible. 
El modelo de usuarios almacena información básica de las personas registradas en la página, como nombre de usuario, correo y contraseña. También existen modelos como ingredientes y categorías, que ayudan a organizar mejor los productos y mostrar información más detallada al cliente.

El sistema también incluye modelos relacionados con las compras y la interacción de los usuarios dentro de la página. El carrito de compras permite guardar los productos seleccionados antes de finalizar una compra, mientras que las reseñas permiten que los clientes puedan compartir opiniones y calificaciones sobre los productos de la pastelería.
Toda esta estructura permite que la información esté mejor organizada y conectada dentro de la aplicación.

Gracias a esto, el sistema puede realizar funciones como registrar usuarios, mostrar productos, administrar pedidos, guardar reseñas y controlar el carrito de compras de manera más eficiente.
Además, el diseño de la base de datos está pensado para representar una situación real dentro de una tienda o pastelería en línea, donde existen usuarios que compran productos, productos que pertenecen a categorías y productos que contienen diferentes ingredientes. Esto ayuda a que el sistema sea más funcional y fácil de administrar.

En general, el diseño de la base de datos es una de las partes más importantes del proyecto, ya que permite que toda la información del sistema se almacene correctamente y que cada parte de la aplicación pueda interactuar entre sí de manera adecuada.



==========ADMINISTRACIÓN DEL SISTEMA==========

Desde este apartado se pueden manejar los diferentes modelos del proyecto, como usuarios, productos, categorías, ingredientes, reseñas y carrito de compras. 
A continuación se muestra el código completo del archivo admin.py del proyecto "Dulce Delirio", que es el responsable de que los administradores puedan gestionar toda la información de manera visual y lógica: 

# pastelería/admin.py
from django.contrib import admin
from .models import User, Category, Product, Cart, CartItem, Ingredient, Review, Order, Payment



====== Admin para usuarios ======= 

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_seller')  # Columnas visibles
    list_filter = ('is_seller',)                       # Filtros laterales
    search_fields = ('username', 'email')              # Barra de búsqueda


 ====== Admin para categoria ====== 

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)




 ====== Admin para ingredientes ====== 

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_allergen', 'allergen_type')
    list_filter = ('is_allergen',)
    search_fields = ('name',)



 ====== Admin para productos ====== 

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ('created_at',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Columnas que se muestran en la lista
    list_display = ('name', 'price', 'stock', 'size', 'flavor', 'is_available', 'owner')
   
    # Filtros laterales para búsqueda rápida
    list_filter = ('categories', 'size', 'flavor', 'is_available')
   
    # Barra de búsqueda
    search_fields = ('name', 'flavor')
   
    # Para relaciones ManyToMany (interfaz mejorada)
    filter_horizontal = ('ingredients',)
   
    # Mostrar reseñas dentro del producto
    inlines = [ReviewInline]
   
    # Campos que se muestran al editar
    fields = ('name', 'description', 'image', 'price', 'stock',
              'size', 'flavor', 'preparation_time', 'is_available',
              'categories', 'ingredients', 'owner')

              

 ====== Admin para carrito ====== 

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    inlines = [CartItemInline]



 ====== Admin para reseñas ====== 

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'comment')



 ====== Admin para pedidos ====== 

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('user__username', 'id')
    readonly_fields = ('created_at', 'updated_at')



==========ENTRADA DE DATOS==========

def product_create(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        product = form.save(commit=False)
        product.owner = request.user
        product.save()

La entrada de datos se realiza desde el panel de administración de Django, donde el administrador puede agregar nueva información al sistema. Por ejemplo, se pueden registrar nuevos productos, crear categorías, agregar ingredientes o incluso gestionar usuarios. Estos datos se almacenan automáticamente en la base de datos y quedan disponibles dentro de la aplicación.

==========ELIMINACIÓN DE DATOS==========

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()

La eliminación de datos también se realiza desde el admin. El administrador puede eliminar registros que ya no sean necesarios o que ya no se utilicen en la página, como productos descontinuados, reseñas incorrectas o información que ya no sea relevante. Esto ayuda a mantener la base de datos organizada y actualizada.



==========ACTUALIZACIÓN DE DATOS==========

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()

La actualización de datos permite modificar información ya existente dentro del sistema. Por ejemplo, se puede cambiar el precio de un producto, actualizar su descripción, modificar la cantidad en stock o editar información de usuarios. Esto permite que la información siempre esté correcta dentro de la aplicación.
    fields = ('name', 'description', 'image', 'price', 'stock',
              'size', 'flavor', 'preparation_time', 'is_available',
              'categories', 'ingredients', 'owner')

==========FUNCIONAMIENTO DE LOS VIEWS Y SUS INTERACCIONES==========

Los views son una parte fundamental del proyecto, ya que se encargan de la lógica de la aplicación. Su función principal es recibir las peticiones del usuario, obtener información de la base de datos mediante los modelos y enviar esos datos a las plantillas para ser mostrados en pantalla.

==========VIEWS Y URLS==========

path('products/create/', views.product_create, name='product_create')
path('products/<uuid:pk>/edit/', views.product_update, name='product_update')
path('products/<uuid:pk>/delete/', views.product_delete, name='product_delete')
Los views trabajan directamente con las URLs, ya que cada URL está conectada a una vista específica. Esto permite que cuando el usuario ingresa a una dirección dentro del sitio web, se ejecute una función concreta que procesa la información correspondiente y determina qué contenido se debe mostrar.

==========VIEWS Y TEMPLATES==========

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = product.reviews.all()
    return render(request, 'pasteleria/product_detail.html', {
        'product': product,
        'reviews': reviews,
    })
Los views también interactúan con los templates, ya que son los encargados de enviar la información que se mostrará en la interfaz del usuario. Los templates reciben estos datos y los presentan de forma visual, permitiendo mostrar productos, formularios, detalles de productos, carrito de compras y otras secciones de manera dinámica.

==========INTEGRACIÓN DEL SISTEMA==========

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

En conjunto, la relación entre models, views, URLs y templates permite el correcto funcionamiento de la aplicación. Los modelos almacenan la información, los views la procesan, las URLs dirigen las solicitudes y los templates muestran la interfaz al usuario, logrando así un sistema completo, organizado y funcional.
En pocas palabras 
URLs = La dirección que escribe el usuario
Views = La lógica que procesa la petición
Templates = El HTML que muestra la información
El flujo es siempre el mismo: URL → View → Template → Usuario. La vista recibe la petición de la URL, consulta la base de datos si es necesario, y envía los datos al template para que se muestren en pantalla.



| Componente | Función | Código clave |
| :--- | :--- | :--- |
| `urls.py` | Recibe la URL y decide qué vista ejecutar | `path('ruta/', views.funcion, name='nombre')` |
| `views.py` | Procesa datos, consulta BD, prepara respuesta | `def funcion(request): + return render()` |
| `Templates` | Muestra los datos visualmente | `{{ variable }}` y `{% for %}` |




==========CONCLUSIONES FINALES==========

En conclusión, el desarrollo de este proyecto final representó una experiencia muy importante para comprender de manera práctica cómo funciona una aplicación web completa utilizando el framework Django. A través de este sistema se logró desarrollar una plataforma funcional para una pastelería en línea llamada “Dulce Delirio”, integrando herramientas de programación, bases de datos, diseño web y gestión de usuarios dentro de un mismo proyecto.

Durante la elaboración del sistema se aplicaron diferentes conocimientos aprendidos a lo largo del semestre, especialmente sobre el desarrollo backend y la administración de bases de datos relacionales. El proyecto permitió entender cómo Django organiza una aplicación mediante modelos, vistas, urls y templates, logrando que todas las partes trabajen de manera conectada para ofrecer una experiencia funcional al usuario.

Uno de los aspectos más importantes del proyecto fue el diseño de la base de datos. Se crearon distintos modelos para representar las entidades principales de la pastelería, como usuarios, productos, categorías, ingredientes, reseñas, carritos, pedidos y pagos. Cada modelo fue diseñado con campos específicos para almacenar información importante dentro del sistema. 
Gracias a esto, la aplicación puede manejar correctamente datos relacionados con productos de repostería, clientes y procesos de compra.

Además, se implementaron distintos tipos de relaciones entre tablas, como relaciones uno a muchos, muchos a muchos y uno a uno. Estas relaciones permitieron conectar correctamente toda la información del sistema.
Por ejemplo, un vendedor puede tener muchos productos, un producto puede pertenecer a varias categorías y un pedido puede tener asociado un único pago. Estas relaciones hacen que la base de datos sea más organizada, eficiente y fácil de administrar.

El proyecto también permitió comprender la importancia de las views dentro de Django. Las views son las encargadas de procesar las solicitudes de los usuarios, obtener información de la base de datos y enviarla a los templates para mostrarla en pantalla. Gracias a esto, se logró implementar funciones importantes como el registro de usuarios, inicio de sesión, creación de productos, carrito de compras, sistema de pedidos y simulación de pagos.

Por otra parte, las urls tuvieron un papel fundamental dentro de la aplicación, ya que son las encargadas de conectar las páginas del sistema con las funciones correspondientes. Cada vez que un usuario entra a una página, Django utiliza las urls para dirigir la solicitud hacia la view adecuada. Esto permitió organizar correctamente la navegación de la plataforma y mejorar la estructura general del proyecto.

En cuanto a los templates, estos permitieron crear la interfaz visual de la pastelería utilizando HTML y el sistema de plantillas de Django. 
Gracias a esto, la aplicación puede mostrar información dinámica al usuario, como listas de productos, detalles de pedidos, reseñas y datos del carrito de compras. Los templates ayudan a que el sistema sea más visual, ordenado y fácil de utilizar para los clientes.

Otro aspecto importante fue la implementación de Django Admin, herramienta que facilitó enormemente la administración de datos dentro del sistema. Desde el panel de administración fue posible agregar, editar y eliminar información relacionada con productos, categorías, usuarios y pedidos sin necesidad de modificar directamente la base de datos. Esto demuestra cómo Django ofrece herramientas que agilizan el desarrollo y la gestión de aplicaciones web.
La temática de la pastelería “Dulce Delirio” permitió crear un proyecto más creativo y cercano a una situación real. El sistema simula el funcionamiento de una tienda en línea donde los clientes pueden explorar productos, agregar artículos al carrito, realizar pedidos y dejar reseñas sobre los productos comprados. Esto ayudó a comprender cómo funcionan actualmente muchas plataformas de comercio electrónico utilizadas por negocios reales.
De igual manera, el proyecto ayudó a desarrollar habilidades relacionadas con la lógica de programación, la organización de código y la resolución de problemas. Durante el desarrollo se presentaron distintos desafíos, como la conexión entre modelos, el manejo de formularios, el control de permisos de usuarios y la validación de información, los cuales fueron solucionados mediante herramientas y funciones proporcionadas por Django.

Finalmente, este proyecto permitió reforzar los conocimientos adquiridos durante el semestre y demostrar que es posible desarrollar aplicaciones web completas utilizando buenas prácticas de programación y estructuras organizadas. La experiencia obtenida servirá como base para futuros proyectos más avanzados relacionados con desarrollo web, bases de datos y sistemas de comercio electrónico.

En general, el sistema desarrollado cumple correctamente con los objetivos planteados, ofreciendo una plataforma funcional, organizada y dinámica para la administración de una pastelería en línea, integrando tanto la parte visual como la lógica interna de la aplicación de manera eficiente y profesional.
