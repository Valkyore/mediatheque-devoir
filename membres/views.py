from django.shortcuts import render
from bibliotheque.models import Livre, DVD, CD, JeuDePlateau  # Import depuis app biblio

def liste_medias_membre(request):
    medias = list(Livre.objects.all()) + list(DVD.objects.all()) + list(CD.objects.all()) + list(JeuDePlateau.objects.all())
    return render(request, 'membre/medias_liste.html', {'medias': medias})

def menu_membre(request):
    return render(request, 'membre/menu.html')  # Lien vers liste