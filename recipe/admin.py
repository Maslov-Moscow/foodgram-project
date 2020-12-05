from django.contrib import admin
from .models import Favorites, ShopingList, RecepeItem, Ingredient, Recipe,Follow
# Register your models here.
admin.site.register(Recipe)
admin.site.register(ShopingList)
admin.site.register(RecepeItem)
admin.site.register(Ingredient)
admin.site.register(Favorites)
admin.site.register(Follow)