from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import User


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    name = models.CharField(max_length=30, unique=True)
    text = models.TextField(max_length=500)
    picture = models.ImageField(upload_to='images/', blank=True, null=True)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    time = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(900)])
    tag_z = models.BooleanField(default=False)
    tag_o = models.BooleanField(default=False)
    tag_y = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    UNITS = [('sp', 'ст.л.'),
             ('gr', 'грамм'),
             ('ml', 'мл.'),
             ('val', 'шт')]

    ing_name = models.CharField(max_length=30)
    unit = models.CharField(max_length=10, choices=UNITS, blank=False, default='val')

    def __str__(self):
        return self.ing_name


class RecepeItem(models.Model):
    ingr_item = models.ForeignKey(Ingredient, on_delete=models.CASCADE, null=False)
    recept = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='part', null=False)
    value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9999)])

    def __str__(self):
        return f"{self.ingr_item} {self.value} in {self.recept}"


class ShopingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='item')


class Favorites(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    fav_recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='favorite')


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriber')
    follower = models.ForeignKey(User, on_delete=models.CASCADE)
