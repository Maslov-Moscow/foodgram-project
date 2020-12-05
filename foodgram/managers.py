from operator import or_

from django.db.models import Q

from recipe.forms import RecipeItemForm
from recipe.models import Recipe, Ingredient, RecepeItem, Favorites


def tag_helper(tags, personal=None):
    """ Получение рецептов отфильтрованных по тегам
     personal == True сортировка для отдельного юзера"""
    check = lambda tags, meal: meal in tags
    if 'breakfast' in tags and 'lunch' in tags and 'dinner' in tags or tags == '':
        if personal == None:
            return Recipe.objects.order_by('-pub_date')
        else:
            return Recipe.objects.filter(author=personal).order_by('-pub_date')
    finder = []
    if check(tags, 'breakfast'):
        finder.append(Q(tag_z=True))
    if check(tags, 'lunch'):
        finder.append(Q(tag_o=True))
    if check(tags, 'dinner'):
        finder.append(Q(tag_y=True))
    if len(finder) == 1:
        if personal == None:
            return Recipe.objects.filter(finder[0]).order_by('-pub_date')
        else:
            return Recipe.objects.filter(finder[0], author=personal).order_by('-pub_date')
    else:
        if personal == None:
            return Recipe.objects.filter(or_(finder[0], finder[1])).order_by('-pub_date')
        else:
            return Recipe.objects.filter(or_(finder[0], finder[1]), author=personal).order_by('-pub_date')


def on_to_True(inp):
    """ маппинг респонса от явы  """
    try:
        if inp == 'on':
            return True
        else:
            return False
    except Exception:
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
            else:
                print(form.errors)
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
