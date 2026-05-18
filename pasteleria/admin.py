# store/admin.py
from django.contrib import admin
from .models import User, Category, Product, Cart, CartItem, Ingredient, Review

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_seller')
    list_filter = ('is_seller',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_allergen', 'allergen_type')
    list_filter = ('is_allergen',)
    search_fields = ('name',)

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ('created_at',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'size', 'flavor', 'is_available', 'owner')
    list_filter = ('categories', 'size', 'flavor', 'is_available')
    search_fields = ('name', 'flavor')
    filter_horizontal = ('ingredients',)  # Mejor interfaz para ManyToMany
    inlines = [ReviewInline]

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    inlines = [CartItemInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'comment')