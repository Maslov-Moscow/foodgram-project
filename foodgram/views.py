from operator import or_

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, get_object_or_404, HttpResponse, redirect

from recipe.forms import RecipeForm
from recipe.models import Recipe, RecepeItem, ShopingList, Favorites, Follow
from users.models import User
from .forms import CreationForm
from .managers import tag_helper, on_to_True, ingridient_adder, tag_helper_fav


def signup(request):
    """ Регистрация    """
    form = CreationForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect("index")
    return render(request, "signup.html", {"form": form})


def index(request):
    """ Главная страница """
    tags = request.GET.get('tags', default='breakfastlunchdinner')
    recipe_list = tag_helper(tags)
    if request.user.is_authenticated:
        fav = Favorites.objects.filter(owner=request.user).select_related('fav_recipe')
        fav_recipes = []
        for x in fav:
            fav_recipes.append(x.fav_recipe.id)

        shop = ShopingList.objects.filter(user=request.user).select_related('recipe')
        shop_recipes = []
        for x in shop:
            shop_recipes.append(x.recipe.id)

    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    if request.user.is_authenticated:
        return render(request, 'IndexAuthD.html',
                      {'page': page, 'paginator': paginator, 'tags': tags, 'fav': fav_recipes, 'shop': shop_recipes,
                       'cnt': len(shop)})
    else:
        return render(request, 'IndexNotAuthD.html', {'page': page, 'paginator': paginator, 'tags': tags})


def author(request, id):
    """ Страница автора  """
    author = get_object_or_404(User, id=id)
    tags = request.GET.get('tags', default='breakfastlunchdinner')
    recipe_list = tag_helper(tags, author)
    if request.user.is_authenticated:

        fav = Favorites.objects.filter(owner=request.user).select_related('fav_recipe')
        fav_recipes = []
        for x in fav:
            fav_recipes.append(x.fav_recipe.id)

        shop = ShopingList.objects.filter(user=request.user).select_related('recipe')

        shop_recipes = []
        for x in shop:
            shop_recipes.append(x.recipe.id)

        follow = Follow.objects.filter(user=request.user, follower=author).exists()

    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    if request.user.is_authenticated:
        return render(request, 'AuthorAuthD.html',
                      {'page': page, 'paginator': paginator, 'tags': tags, 'fav': fav_recipes, 'shop': shop_recipes,
                       'cnt': len(shop), 'author': author, 'follow': follow})
    else:
        return render(request, 'AuthorAuthD.html',
                      {'page': page, 'paginator': paginator, 'tags': tags, 'author': author})


@login_required
def subscribes(request):
    """ Странница подписок"""
    cnt = ShopingList.objects.filter(user=request.user).count()
    follows = Follow.objects.filter(user=request.user).select_related('follower')

    authors = []  # User object
    for x in follows:
        authors.append(User.objects.get(id=x.follower.id))

    paginator = Paginator(authors, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'myFollow.html', {'cnt': cnt, 'page': page, 'paginator': paginator})


@login_required
def newrecipe(request):
    cnt = ShopingList.objects.filter(user=request.user).count()
    if request.method == 'GET':
        return render(request, 'formRecipe.html', {'cnt': cnt})
    else:
        form = RecipeForm(
            {'name': request.POST['name'], 'text': request.POST['description'], 'time': request.POST['time'],
             'tag_y': on_to_True(request.POST.get('dinner')), 'tag_o': on_to_True(request.POST.get('lunch')),
             'tag_z': on_to_True(request.POST.get('breakfast'))}, request.FILES or None)
        if 'valueIngredient_1' not in request.POST:
            return render(request, 'formRecipe.html', {'form': form, "msg": 'Добавте ингридиенты', 'cnt': cnt})
        if form.is_valid():
            if form.cleaned_data['tag_y'] == False and form.cleaned_data['tag_z'] == False and form.cleaned_data[
                'tag_o'] == False:
                return render(request, 'formRecipe.html', {'form': form, "msg2": 'Добавте хотябы один тег', 'cnt': cnt})
            recipe = form.save(commit=False)
            recipe.author = request.user
            try:
                recipe.picture = request.FILES['file']
            except Exception:
                pass
            recipe.save()
            ingridient_adder(request, recipe, True)
            return redirect('index')
        return render(request, 'formRecipe.html', {'form': form, 'cnt': cnt}, )


@login_required
def recipe_edit(request, id):
    """ Редактирование рецепта """
    cnt = ShopingList.objects.filter(user=request.user).count()
    recipe = get_object_or_404(Recipe, id=id)
    if request.user == recipe.author:
        if request.method == 'POST':
            form = RecipeForm(
                {'name': request.POST['name'], 'text': request.POST['description'], 'time': request.POST['time'],
                 'tag_y': on_to_True(request.POST.get('dinner')), 'tag_o': on_to_True(request.POST.get('lunch')),
                 'tag_z': on_to_True(request.POST.get('breakfast'))}, request.FILES or None, instance=recipe)
            if form.is_valid():
                recipe = form.save(commit=False)
                recipe.author = request.user
                try:
                    recipe.picture = request.FILES['file']
                except Exception:
                    pass
                recipe.save()
                ingridient_adder(request, recipe, False)
                return redirect(f'/recipe/{recipe.id}')
            else:
                return render(request, 'formRecipe.html', {'form': form, 'cnt': cnt})

        else:
            form = RecipeForm(instance=recipe)
            return render(request, 'formRecipe edit.html', {'cnt': cnt, 'recipe': recipe})
    else:
        raise Http404()


@login_required
def favorites(request):
    tags = request.GET.get('tags', default='breakfastlunchdinner')
    recipe_list = tag_helper_fav(tags, request.user)

    cnt = ShopingList.objects.filter(user=request.user).count()

    shop = ShopingList.objects.filter(user=request.user).select_related('recipe')
    shop_recipes = []
    for x in shop:
        shop_recipes.append(x.recipe.id)

    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'favorite.html',
                  {'page': page, 'paginator': paginator, 'tags': tags, 'cnt': cnt, 'shop': shop_recipes})


@login_required
def get_shop(request):
    """ Создание списка продуктов """
    shop_list = ShopingList.objects.filter(user=request.user).select_related('recipe')
    recipe = []
    for x in shop_list:
        recipe.append(x.recipe)

    ingridients = []
    for x in recipe:
        y = RecepeItem.objects.filter(recept=x)
        ingridients.append(y)

    temp = ingridients[0]  # <QuerySet [<RecepeItem>]
    for x in range(1, len(ingridients)):
        temp = or_(temp, ingridients[x])

    data = ['Список покупок:\n']
    for x in temp:
        data.append(f'\n{x.ingr_item.ing_name} {x.value} {x.ingr_item.get_unit_display()} ')

    file_data = data
    response = HttpResponse(file_data, content_type='application/text charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="shop list.txt"'
    return response


@login_required
def shop_list(request):
    """ Список покупок"""
    shop_list = ShopingList.objects.filter(user=request.user).select_related('recipe')
    cards = []
    for x in shop_list:
        cards.append(x.recipe)
    return render(request, 'shopList.html', {'cards': cards, 'cnt': len(shop_list)})


def singlePage(request, id):
    """Страница рецепта"""
    recipe = Recipe.objects.get(id=id)
    if request.user.is_authenticated:
        cnt = ShopingList.objects.filter(user=request.user).count()
        # проверка на избранное
        fav = Favorites.objects.filter(owner=request.user).select_related('fav_recipe')
        fav_recipes = []
        for x in fav:
            fav_recipes.append(x.fav_recipe.id)
        # проверка на список покупок
        shop = ShopingList.objects.filter(user=request.user).select_related('recipe')
        shop_recipes = []
        for x in shop:
            shop_recipes.append(x.recipe.id)
        # получение ингридиентов
        items = RecepeItem.objects.filter(recept=recipe)

        # проверка на авторство
        owner = recipe.author == request.user

        # под писка на автора
        follow = Follow.objects.filter(user=request.user, follower=recipe.author).exists()

        return render(request, 'singlePage.html',
                      {'card': recipe, 'count': cnt, 'items': items, 'shop': shop_recipes, 'fav': fav_recipes,
                       'owner': owner, 'follow': follow})
    else:
        items = RecepeItem.objects.filter(recept=recipe)
        return render(request, 'singlePage.html', {'card': recipe, 'items': items})
