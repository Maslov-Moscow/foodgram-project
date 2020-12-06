from recipe.models import Favorites, ShopingList


def favorites(request):
    if request.user.is_authenticated:
        fav = Favorites.objects.filter(owner=request.user).select_related('fav_recipe')
        fav_recipes = []
        for x in fav:
            fav_recipes.append(x.fav_recipe.id)
        return {'fav': fav_recipes}
    else:
        pass


def shop(request):
    if request.user.is_authenticated:
        shop = ShopingList.objects.filter(user=request.user).select_related('recipe')
        shop_recipes = []
        for x in shop:
            shop_recipes.append(x.recipe.id)
        return {'shop': shop_recipes, 'cnt': len(shop_recipes)}
    else:
        pass
