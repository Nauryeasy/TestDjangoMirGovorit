from django.contrib import admin
from main.models import *

class ProductWeightInline(admin.TabularInline):
    model = ProductWeight
    extra = 1  # Количество пустых форм для добавления новых объектов

class RecipeAdmin(admin.ModelAdmin):
    inlines = [ProductWeightInline]

admin.site.register(Recipe, RecipeAdmin)

admin.site.register(Product)
admin.site.register(ProductWeight)
