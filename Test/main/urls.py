from django.urls import path, include
from .views import *

urlpatterns = [
    path('add-product-to-recipe', AddProductToRecipe.as_view()),
    path('cook-recipe', CookRecipe.as_view()),
    path('show_recipes_without_product', ShowRecipesWithoutProduct.as_view()),
]
