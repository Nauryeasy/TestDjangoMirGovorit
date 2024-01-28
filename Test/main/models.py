from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    usage_counter = models.PositiveIntegerField(default=0)


class Recipe(models.Model):
    name = models.CharField(max_length=100)


class ProductWeight(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    weight = models.PositiveIntegerField(null=False, verbose_name='Вес в граммах')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
