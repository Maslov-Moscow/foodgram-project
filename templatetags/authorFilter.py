from django import template
from recipe.models import User
register = template.Library()


@register.filter 
def countRecipe(username):
    count = Recipe.objects.filter(author__username=username).count()
    if count > 3:
        pass
    else:
        return f"Еще {(count - 3)} рецептов..."