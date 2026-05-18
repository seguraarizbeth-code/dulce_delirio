# store/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseForbidden
from .forms import ProductForm, RegisterForm
from .models import Product, Cart, CartItem, Category

def home(request):
    """Vista principal con buscador, filtro por categoría y paginación."""
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    size_filter = request.GET.get('size')
    flavor_query = request.GET.get('flavor')

    products = Product.objects.select_related('owner').prefetch_related('categories').all()

    # Búsqueda por nombre o descripción
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    # Filtro por categoría
    if category_id:
        products = products.filter(categories__id=category_id)

    # Filtro por tamaño
    if size_filter:
        products = products.filter(size=size_filter)

    # Filtro por sabor
    if flavor_query:
        products = products.filter(flavor__icontains=flavor_query)

    # Paginación: 6 productos por página
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    # Tamaños para el filtro
    size_choices = Product.SIZE_CHOICES

    return render(request, 'pasteleria/home.html', {
        'page_obj': page_obj,
        'categories': categories,
        'size_choices': size_choices,
        'products': products, # Pasamos todos para que el conteo sea correcto, aunque page_obj tiene los de la página actual.
    })

def register(request):
    """Registro de nuevos usuarios."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'pasteleria/register.html', {'form': form})

def login_view(request):
    """Inicio de sesión."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            # Redirige al dashboard si es vendedor, si no, a home
            return redirect('dashboard' if user.is_seller else 'home')
    return render(request, 'pasteleria/login.html')

def logout_view(request):
    """Cierre de sesión."""
    logout(request)
    return redirect('home')

# =========================
# 📋 Dashboard (Solo Vendedores)
# =========================
@login_required
def dashboard(request):
    """Panel de control para administradores/vendedores."""
    if not request.user.is_seller:
        return HttpResponseForbidden("No tienes permisos para acceder a esta página.")
    products = Product.objects.filter(owner=request.user)
    return render(request, 'pasteleria/dashboard.html', {'products': products})

# =========================
# ➕ CRUD de Productos
# =========================
@login_required
def product_create(request):
    """Crear un nuevo producto."""
    if not request.user.is_seller:
        return HttpResponseForbidden("Solo los vendedores pueden crear productos.")
    form = ProductForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        product = form.save(commit=False)
        product.owner = request.user
        product.save()
        form.save_m2m() # Guarda las relaciones ManyToMany (categorías)
        return redirect('dashboard')
    return render(request, 'pasteleria/product_form.html', {'form': form, 'action': 'Crear'})

@login_required
def product_update(request, pk):
    """Editar un producto existente."""
    product = get_object_or_404(Product, pk=pk)
    if product.owner != request.user:
        return HttpResponseForbidden("No puedes editar este producto.")
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('dashboard')
    return render(request, 'pasteleria/product_form.html', {'form': form, 'action': 'Editar'})

@login_required
def product_delete(request, pk):
    """Eliminar un producto."""
    product = get_object_or_404(Product, pk=pk)
    if product.owner != request.user:
        return HttpResponseForbidden("No puedes eliminar este producto.")
    if request.method == 'POST':
        product.delete()
        return redirect('dashboard')
    return render(request, 'pasteleria/product_confirm_delete.html', {'product': product})

def product_detail(request, pk):
    """Ver el detalle de un producto."""
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'pasteleria/product_detail.html', {'product': product})


# =========================
# 🛒 Carrito de Compras
# =========================
@login_required
def cart_detail(request):
    """Ver el contenido del carrito."""
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'pasteleria/cart_detail.html', {'cart': cart})

@login_required
def add_to_cart(request, product_id):
    """Añadir un producto al carrito."""
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_detail')

@login_required
def remove_from_cart(request, item_id):
    """Eliminar un artículo del carrito."""
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart_detail')

@login_required
def update_cart_item(request, item_id):
    """Actualizar la cantidad de un artículo en el carrito."""
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            item.quantity = quantity
            item.save()
        else:
            item.delete()
    return redirect('cart_detail')