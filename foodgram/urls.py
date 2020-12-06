"""foodgram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('singup/', views.signup, name="signup"),
    path('recipe/<int:id>/', views.single_page),
    path('edit/<int:id>/', views.recipe_edit),
    path('newrecipe/', views.newrecipe),
    path('shop/', views.shop_list, name='shop'),
    path('getshop/', views.get_shop),  # список покупок
    path('favorite/', views.favorites),
    path('author/<int:id>', views.author),
    path('follow/', views.subscribes, name='follow'),
    path('api/', include('api.urls')),
    path("auth/", include("django.contrib.auth.urls"))

]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
