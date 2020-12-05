from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()


class CreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=50,required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name",  "username", "email")
