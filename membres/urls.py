from django.urls import path
from . import views

urlpatterns = [
    path('medias/', views.liste_medias_membre, name='liste_medias_membre'),
    path('menu/', views.menu_membre, name='menu_membre'),
]