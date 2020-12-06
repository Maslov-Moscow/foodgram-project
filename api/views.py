from .serializers import IngridientSerilaizer, CommonIdSerializer
from recipe.models import Ingredient, Favorites, Recipe, ShopingList, Follow, User

from rest_framework.views import APIView
from rest_framework.response import Response



class InridientFinder(APIView):
    def get(self, request):
        query = request.GET['query']
        ingridients = Ingredient.objects.filter(ing_name__startswith=query)
        serializer = IngridientSerilaizer(ingridients, many=True)
        return Response(serializer.data)


class Favorit(APIView):
    def post(self, request):
        serializer = CommonIdSerializer(data=request.data)
        if serializer.is_valid():
            id = serializer.data.get('id')
            recipe = Recipe.objects.get(id=id)
            Favorites.objects.create(owner=request.user, fav_recipe=recipe)
        return Response({"success": True})


class FavoritRemove(APIView):
    def delete(self, request, id):
        recipe = Recipe.objects.get(id=id)
        Favorites.objects.get(fav_recipe=recipe).delete()
        return Response({"success": True})


class PurchasesApi(APIView):

    def get(self, request):
        return Response({"success": True})

    def post(self, request):
        serializer = CommonIdSerializer(data=request.data)
        if serializer.is_valid():
            id = serializer.data.get('id')
            recipe = Recipe.objects.get(id=id)
            ShopingList.objects.create(recipe=recipe, user=request.user)
        return Response({"success": True})


class PurchasesApiRemove(APIView):
    def delete(self, request, id):
        recipe = Recipe.objects.get(id=id)
        ShopingList.objects.get(recipe=recipe).delete()
        return Response({"success": True})


class SubscriptionsApi(APIView):
    def post(self, request):
        serializer = CommonIdSerializer(data=request.data)
        if serializer.is_valid():
            id = serializer.data.get('id')
            follow = User.objects.get(id=id)
            Follow.objects.create(user=request.user, follower=follow)
            return Response({"success": True})


class SubscriptionsApiRemove(APIView):
    def delete(self, request, id):
        try:
            user = request.user
            follower = User.objects.get(id=id)
            Follow.objects.filter(user=request.user, follower=follower).delete()
            return Response({"success": True})
        except Exception:
            return Response({'succes': False})

