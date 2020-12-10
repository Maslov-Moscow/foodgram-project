from operator import or_

from django.db.models import Q

from recipe.forms import RecipeItemForm
from recipe.models import Recipe, Ingredient, RecepeItem, Favorites


def tag_helper(tags, personal=None):
    """ Получение рецептов отфильтрованных по тегам
     personal == True сортировка для отдельного юзера"""
    check = lambda tags, meal: meal in tags
    recipes = Recipe.objects.order_by('-pub_date')
    if personal is not None:
        recipes = recipes.filter(author=personal)

    if 'breakfast' in tags and 'lunch' in tags and 'dinner' in tags or tags == '':
        return recipes

    finder = []
    if check(tags, 'breakfast'):
        finder.append(Q(tag_z=True))
    if check(tags, 'lunch'):
        finder.append(Q(tag_o=True))
    if check(tags, 'dinner'):
        finder.append(Q(tag_y=True))
    if len(finder) == 1:
        return recipes.filter(finder[0])
    else:
        return recipes.filter(or_(finder[0], finder[1]))


def on_to_True(inp):
    """ маппинг респонса от явы  """
    if inp == 'on':
        return True
    else:
        return False


def ingridient_adder(request, recipe, new):
    """добавляем или создаём игридиент в рецепте """
    if new == True:
        counter = 1
        while request.POST.get(f'valueIngredient_{counter}') != None:
            item = Ingredient.objects.get_or_create(ing_name=request.POST.get(f'nameIngredient_{counter}'))
            form = RecipeItemForm(
                {'ingr_item': item[0], 'recept': recipe, 'value': int(request.POST.get(f'valueIngredient_{counter}'))})
            if form.is_valid():
                form.save(commit=True)

            counter += 1
    else:
        if request.POST.get(f'valueIngredient_1') == None:
            pass
        else:
            RecepeItem.objects.filter(recept=recipe).delete()
            ingridient_adder(request=request, recipe=recipe, new=True)


def tag_helper_fav(tags, user):
    """Фильтрация по тегам в избранном"""
    recipes = list()
    for f in Favorites.objects.filter(owner=user).select_related('fav_recipe'):
        recipes.append(f.fav_recipe)
    check = lambda tags, meal: meal in tags
    if 'breakfast' in tags and 'lunch' in tags and 'dinner' in tags or tags == '':
        return recipes
    filtred = list()
    if check(tags, 'breakfast'):
        for recipe in recipes:
            if recipe.tag_z == True and recipe not in filtred:
                filtred.append(recipe)
    if check(tags, 'lunch'):
        for recipe in recipes:
            if recipe.tag_o == True and recipe not in filtred:
                filtred.append(recipe)
    if check(tags, 'dinner'):
        for recipe in recipes:
            if recipe.tag_y == True and recipe not in filtred:
                filtred.append(recipe)
    return filtred
