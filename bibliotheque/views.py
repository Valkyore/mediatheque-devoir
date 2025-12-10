from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Emprunteur, Livre, DVD, CD, JeuDePlateau, Emprunt
from django.core.exceptions import ValidationError
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('menu_biblio')
        messages.error(request, 'Login invalide.')
    return render(request, 'biblio/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def home(request):
    return render(request, 'home.html', {'is_logged': request.user.is_authenticated})

@login_required
def liste_membres(request):
    membres = Emprunteur.objects.all()
    return render(request, 'biblio/membres_liste.html', {'membres': membres})

@login_required
def creer_membre(request):
    if request.method == 'POST':
        nom = request.POST.get('nom', '').strip()
        if nom:
            Emprunteur.objects.create(nom=nom)
            return redirect('liste_membres')
        return HttpResponse("Erreur : Nom requis.")
    return render(request, 'biblio/creer_membre.html')

@login_required
def delete_membre(request, pk):
    membre = get_object_or_404(Emprunteur, pk=pk)
    if request.method == 'POST':
        membre.delete()
        return redirect('liste_membres')
    return render(request, 'biblio/confirm_delete.html', {'membre': membre})

@login_required
def update_membre(request, pk):
    membre = get_object_or_404(Emprunteur, pk=pk)
    if request.method == 'POST':
        nom = request.POST.get('nom', '').strip()
        if nom:
            membre.nom = nom
            membre.save()
            return redirect('liste_membres')
        return HttpResponse("Erreur : Nom requis.")
    return render(request, 'biblio/update_membre.html', {'membre': membre})


def liste_medias(request):
    medias = list(Livre.objects.all()) + list(DVD.objects.all()) + list(CD.objects.all()) + list(JeuDePlateau.objects.all())
    all_membres = Emprunteur.objects.all()
    membres = [m for m in all_membres if m.peut_emprunter()]
    return render(request, 'biblio/medias_liste.html', {'medias': medias, 'membres': membres})

@login_required
def ajouter_media(request):
    if request.method == 'POST':
        type_m = request.POST.get('type')
        nom = request.POST.get('nom', '').strip()
        if not nom:
            return HttpResponse("Erreur : Nom requis.")
        auteur = ''
        if type_m == 'Livre':
            try:
                response = requests.get(f"https://openlibrary.org/search.json?q={nom}")
                if response.status_code == 200:
                    data = response.json()
                    if data['docs']:
                        auteur = data['docs'][0]['author_name'][0] if data['docs'][0].get('author_name') else request.POST.get('auteur', '')
                    else:
                        auteur = request.POST.get('auteur', '')
                else:
                    auteur = request.POST.get('auteur', '')
            except Exception as e:
                auteur = request.POST.get('auteur', '')
            Livre.objects.create(nom=nom, auteur=auteur)
        elif type_m == 'DVD':
            realisateur = request.POST.get('realisateur', '')
            DVD.objects.create(nom=nom, realisateur=realisateur)
        elif type_m == 'CD':
            artiste = request.POST.get('artiste', '')
            CD.objects.create(nom=nom, artiste=artiste)
        elif type_m == 'Jeu':
            createur = request.POST.get('createur', '')
            JeuDePlateau.objects.create(nom=nom, createur=createur)
        return redirect('liste_medias')
    return render(request, 'biblio/ajouter_media.html')

@login_required
def creer_emprunt(request, media_pk, media_type, emprunteur_pk):
    if request.method == 'POST':
        emprunteur_pk = request.POST.get('emprunteur_pk')
        if not emprunteur_pk:
            return HttpResponse("Erreur : Sélectionnez un membre.")
        emprunteur = get_object_or_404(Emprunteur, pk=emprunteur_pk)
    else:
        emprunteur = get_object_or_404(Emprunteur, pk=emprunteur_pk)
    media = None
    if media_type == 'Livre':
        media = get_object_or_404(Livre, pk=media_pk)
        emprunt = Emprunt(emprunteur=emprunteur, livre=media)
    elif media_type == 'DVD':
        media = get_object_or_404(DVD, pk=media_pk)
        emprunt = Emprunt(emprunteur=emprunteur, dvd=media)
    elif media_type == 'CD':
        media = get_object_or_404(CD, pk=media_pk)
        emprunt = Emprunt(emprunteur=emprunteur, cd=media)
    else:
        return HttpResponse("Type média invalide.")
    try:
        emprunt.save()
        return redirect('liste_medias')
    except ValidationError as e:
        return HttpResponse(f"Erreur emprunt : {e}")

@login_required
def liste_emprunts(request):
    emprunts = Emprunt.objects.filter(retourne=False)
    return render(request, 'biblio/emprunts_liste.html', {'emprunts': emprunts})

@login_required
def rentrer_emprunt(request, pk):
    emprunt = get_object_or_404(Emprunt, pk=pk)
    emprunt.retourner()
    return redirect('liste_medias')

@login_required
def menu_biblio(request):
    return render(request, 'biblio/menu.html')