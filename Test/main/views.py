from django.db.models import Q
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from rest_framework import views
from rest_framework.response import Response

from .models import *


class AddProductToRecipe(views.APIView):
    def get(self, request, *args, **kwargs):
        recipe_id = request.GET.get('recipe_id')
        product_id = request.GET.get('product_id')
        weight = request.GET.get('weight')

        if weight is None:
            return Response({'error': 'weight parameters must be filled in'}, status=400)

        try:
            recipe = Recipe.objects.get(id=recipe_id)
            product = Product.objects.get(id=product_id)
        except Recipe.DoesNotExist:
            return Response({'error': 'recipe not found'}, status=404)
        except Product.DoesNotExist:
            return Response({'error': 'product not found'}, status=404)

        product_in_recipe = recipe.productweight_set.filter(product=product)

        if product_in_recipe.exists():
            product_in_recipe.update(weight=weight)
            return Response({'error': 'weight is updated'}, status=200)

        product_weight = ProductWeight(
            product=product,
            weight=weight,
            recipe=recipe,
        )
        product_weight.save()

        return Response({'status': 'ok'}, status=200)


class CookRecipe(views.APIView):
    def get(self, request, *args, **kwargs):
        recipe_id = request.GET.get('recipe_id')

        try:
            recipe = Recipe.objects.get(id=recipe_id)
        except:
            return Response({'error': 'recipe not found'}, status=404)

        products_in_recipe = recipe.productweight_set.all()

        for product in products_in_recipe:
            product.product.usage_counter += 1
            product.product.save()

        return Response({'status': 'ok'}, status=200)


class ShowRecipesWithoutProduct(View):
    def get(self, request, *args, **kwargs):
        product_id = request.GET.get('product_id')

        try:
            product = Product.objects.get(id=product_id)
        except:
            return Response({'error': 'product not found'}, status=404)

        recipes = Recipe.objects.filter(~Q(productweight__product=product) | Q(productweight__product=product, productweight__weight__lt=10))
        result = recipes.values('id', 'name').distinct()

        return render(request, 'list.html', {'result': result}, status=200)
