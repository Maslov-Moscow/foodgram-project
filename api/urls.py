from django.urls import path

from . import views

urlpatterns = [
    path('inridient-item/', views.InridientFinder.as_view()),
    path('favorites/', views.Favorit.as_view()),
    path('favorites/<int:id>/', views.FavoritRemove.as_view()),
    path('purchases/', views.PurchasesApi.as_view()),
    path('purchases/<int:id>/', views.PurchasesApiRemove.as_view()),
    path('subscriptions/', views.SubscriptionsApi.as_view()),
    path('subscriptions/<int:id>/', views.SubscriptionsApiRemove.as_view())
]
