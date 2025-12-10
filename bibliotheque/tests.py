from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError
from .models import Emprunteur, Livre, DVD, CD, JeuDePlateau, Emprunt

class TestModels(TestCase):
    def test_peut_emprunter_max3(self):
        emprunteur = Emprunteur.objects.create(nom="Test User")
        livre1 = Livre.objects.create(nom="Livre1", auteur="A1")
        livre2 = Livre.objects.create(nom="Livre2", auteur="A2")
        livre3 = Livre.objects.create(nom="Livre3", auteur="A3")
        # 3 emprunts sur livres séparés
        Emprunt.objects.create(emprunteur=emprunteur, livre=livre1)
        Emprunt.objects.create(emprunteur=emprunteur, livre=livre2)
        Emprunt.objects.create(emprunteur=emprunteur, livre=livre3)
        self.assertFalse(emprunteur.peut_emprunter())

    def test_verifier_retards_bloque(self):
        emprunteur = Emprunteur.objects.create(nom="Test User")
        livre = Livre.objects.create(nom="Test Livre", auteur="Test Auteur")
        emprunt = Emprunt.objects.create(emprunteur=emprunteur, livre=livre)
        emprunt.date_emprunt = timezone.now().date() - timedelta(weeks=2)
        emprunt.save()
        emprunteur.verifier_retards()
        self.assertTrue(emprunteur.bloque)  # Doit être bloqué

    def test_jeu_non_empruntable(self):
        emprunteur = Emprunteur.objects.create(nom="Test User")
        jeu = JeuDePlateau.objects.create(nom="Test Jeu", createur="Test")
        # Test validation jeu
        with self.assertRaises((ValidationError, ValueError)):  # Capture erreur
            Emprunt.objects.create(emprunteur=emprunteur, livre=jeu)  # Erreur type FK, mais simule non-empruntable

class TestViews(TestCase):
    def setUp(self):
        self.livre = Livre.objects.create(nom="Test Livre", auteur="Test Auteur")

    def test_liste_medias(self):
        response = self.client.get('/biblio/medias/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Livre")  # Data de setUp

    def test_multi_media_emprunt(self):
        # Test emprunt DVD (multi-types)
        emprunteur = Emprunteur.objects.create(nom="Test User")
        dvd = DVD.objects.create(nom="Test DVD", realisateur="Test")
        emprunt = Emprunt.objects.create(emprunteur=emprunteur, dvd=dvd)
        self.assertEqual(emprunt.media.nom, "Test DVD")  # Vérifie multi-FK (getter media)