from django import forms
from .models import Recipe, Ingredient, RecepeItem
from django.utils.translation import gettext_lazy as _


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('name','text','time','tag_z','tag_o','tag_y','picture')
        labels = {
            'text': _('Описание'),'name':_('Название рецепта'),'time': _('Время приготовления')
        }
        error_messages = {
            'name': {
                'unique': _("Рецепт с таким именем существует!"),
            },
        }
     


class IngridientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ('__all__')

class RecipeItemForm(forms.ModelForm):
    class Meta:
        model = RecepeItem
        fields = ('__all__')