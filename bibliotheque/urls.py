from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('membres/', views.liste_membres, name='liste_membres'),
    path('membre/creer/', views.creer_membre, name='creer_membre'),
    path('membre/<int:pk>/delete/', views.delete_membre, name='delete_membre'),
    path('membre/<int:pk>/update/', views.update_membre, name='update_membre'),
    path('medias/', views.liste_medias, name='liste_medias'),
    path('media/ajouter/', views.ajouter_media, name='ajouter_media'),
    path('emprunt/creer/<int:media_pk>/<str:media_type>/<int:emprunteur_pk>/', views.creer_emprunt, name='creer_emprunt'),
    path('emprunt/<int:pk>/rentrer/', views.rentrer_emprunt, name='rentrer_emprunt'),
    path('menu/', views.menu_biblio, name='menu_biblio'),
    path('emprunts/', views.liste_emprunts, name='liste_emprunts'),
]