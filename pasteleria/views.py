from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from django.http import HttpResponseForbidden
from .forms import ProductForm, RegisterForm, ReviewForm
from .models import Product, Cart, CartItem, Category, Ingredient, Review

def home(request):
    """Vista principal con buscador, filtros y paginación."""
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    size_filter = request.GET.get('size')
    flavor_query = request.GET.get('flavor')
    ingredient_filter = request.GET.get('ingredient')

    products = Product.objects.select_related('owner').prefetch_related(
        'categories', 'ingredients', 'reviews'
    ).filter(is_available=True)

    # Búsqueda por nombre o descripción
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(flavor__icontains=query)
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
    
    # Filtro por ingrediente
    if ingredient_filter:
        products = products.filter(ingredients__id=ingredient_filter)

    # Paginación: 6 productos por página
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    size_choices = Product.SIZE_CHOICES
    ingredients = Ingredient.objects.all().order_by('name')

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'size_choices': size_choices,
        'ingredients': ingredients,
    }
    return render(request, 'pasteleria/home.html', context)

def register(request):
    """Registro de nuevos usuarios."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Cuenta creada exitosamente! Bienvenido/a.')
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
            messages.success(request, f'¡Bienvenido/a de nuevo, {user.username}!')
            return redirect('dashboard' if user.is_seller else 'home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'pasteleria/login.html')

def logout_view(request):
    """Cierre de sesión."""
    logout(request)
    messages.info(request, 'Has cerrado sesión.')
    return redirect('home')

# =========================
# 📋 Dashboard (Solo Vendedores)
# =========================
@login_required
def dashboard(request):
    """Panel de control para administradores/vendedores."""
    if not request.user.is_seller:
        return HttpResponseForbidden("No tienes permisos para acceder a esta página.")
    products = Product.objects.filter(owner=request.user).prefetch_related('reviews', 'ingredients')
    total_products = products.count()
    total_reviews = Review.objects.filter(product__owner=request.user).count()
    avg_rating = Review.objects.filter(product__owner=request.user).aggregate(
        avg=Avg('rating')
    )['avg'] or 0
    
    context = {
        'products': products,
        'total_products': total_products,
        'total_reviews': total_reviews,
        'avg_rating': round(avg_rating, 1),
    }
    return render(request, 'pasteleria/dashboard.html', context)

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
        form.save_m2m()
        messages.success(request, f'¡{product.name} creado exitosamente!')
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
        messages.success(request, f'¡{product.name} actualizado exitosamente!')
        return redirect('dashboard')
    return render(request, 'pasteleria/product_form.html', {'form': form, 'action': 'Editar'})

@login_required
def product_delete(request, pk):
    """Eliminar un producto."""
    product = get_object_or_404(Product, pk=pk)
    if product.owner != request.user:
        return HttpResponseForbidden("No puedes eliminar este producto.")
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'"{product_name}" ha sido eliminado.')
        return redirect('dashboard')
    return render(request, 'pasteleria/product_confirm_delete.html', {'product': product})

def product_detail(request, pk):
    """Ver el detalle de un producto con reseñas."""
    product = get_object_or_404(
        Product.objects.prefetch_related('ingredients', 'reviews__user'), 
        pk=pk
    )
    reviews = product.reviews.all()
    user_review = None
    
    # Si el usuario está autenticado y ya dejó una reseña, se la mostramos
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
    
    # Formulario para nueva reseña (solo si no ha dejado una)
    review_form = None
    if request.user.is_authenticated and not user_review:
        if request.method == 'POST':
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.product = product
                review.user = request.user
                review.save()
                messages.success(request, '¡Gracias por tu reseña!')
                return redirect('product_detail', pk=product.id)
        else:
            review_form = ReviewForm()
    
    # Productos relacionados (misma categoría)
    related_products = Product.objects.filter(
        categories__in=product.categories.all()
    ).exclude(id=product.id).distinct()[:4]
    
    context = {
        'product': product,
        'reviews': reviews,
        'user_review': user_review,
        'review_form': review_form,
        'related_products': related_products,
    }
    return render(request, 'pasteleria/product_detail.html', context)

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
    
    if not product.is_in_stock:
        messages.error(request, f'"{product.name}" no está disponible en este momento.')
        return redirect('product_detail', pk=product_id)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f'Se agregó otra unidad de "{product.name}" al carrito.')
        else:
            messages.warning(request, 'No hay suficiente stock disponible.')
    else:
        messages.success(request, f'"{product.name}" agregado al carrito.')
    
    return redirect('cart_detail')

@login_required
def remove_from_cart(request, item_id):
    """Eliminar un artículo del carrito."""
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = item.product.name
    item.delete()
    messages.success(request, f'"{product_name}" eliminado del carrito.')
    return redirect('cart_detail')

@login_required
def update_cart_item(request, item_id):
    """Actualizar la cantidad de un artículo en el carrito."""
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > item.product.stock:
            messages.warning(request, f'Solo hay {item.product.stock} unidades disponibles de "{item.product.name}".')
            quantity = item.product.stock
        
        if quantity > 0:
            item.quantity = quantity
            item.save()
            messages.success(request, 'Cantidad actualizada.')
        else:
            item.delete()
            messages.success(request, 'Producto eliminado del carrito.')
    return redirect('cart_detail')