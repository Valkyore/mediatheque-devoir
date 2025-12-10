from django.db import models
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from django.utils import timezone



class Media(models.Model):
    TYPES = [
        ('Livre', 'Livre'),
        ('DVD', 'DVD'),
        ('CD', 'CD'),
        ('Jeu', 'Jeu de Plateau'),
    ]
    nom = models.CharField(max_length=200)  # Nom du média
    type_media = models.CharField(max_length=20, choices=TYPES)  # Type pour filtrage (empruntable ou non)
    disponible = models.BooleanField(default=True)  # Statut dispo pour emprunt
    date_ajout = models.DateField(auto_now_add=True)  # Date création

    class Meta:
        abstract = True  # Pas de table DB pour ce modèle (héritage seulement)

    def __str__(self):
        return f"{self.nom} ({self.get_type_media_display()})"


class Livre(Media):
    type_media = 'Livre'
    auteur = models.CharField(max_length=100)

class DVD(Media):
    type_media = 'DVD'
    realisateur = models.CharField(max_length=100)

class CD(Media):
    type_media = 'CD'
    artiste = models.CharField(max_length=100)

class JeuDePlateau(Media):
    createur = models.CharField(max_length=100)
    type_media = 'Jeu'  # Fixé : non empruntable


class Emprunteur(models.Model):
    nom = models.CharField(max_length=100)
    bloque = models.BooleanField(default=False)  # Bloqué si retard

    def emprunts_actifs(self):

        return self.emprunts.filter(retourne=False).count()

    def peut_emprunter(self):
        # Logique métier : <3 actifs ET pas bloqué ET pas de retard
        if self.bloque or self.emprunts_actifs() >= 3:
            return False
        self.verifier_retards()  # Check auto-retards
        return not self.bloque

    def verifier_retards(self):
        # Méthode défensive : Vérifie tous emprunts ; bloque si >1 semaine
        for emprunt in self.emprunts.filter(retourne=False):
            if emprunt.date_emprunt + timedelta(weeks=1) < date.today():
                self.bloque = True
                self.save()
                break  # Un seul suffit pour bloquer
        return not self.bloque

    def __str__(self):
        return self.nom


class Emprunt(models.Model):
    emprunteur = models.ForeignKey(Emprunteur, on_delete=models.CASCADE, related_name='emprunts')
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE, null=True, blank=True, related_name='emprunts_livre')
    dvd = models.ForeignKey(DVD, on_delete=models.CASCADE, null=True, blank=True, related_name='emprunts_dvd')
    cd = models.ForeignKey(CD, on_delete=models.CASCADE, null=True, blank=True, related_name='emprunts_cd')
    jeu = models.ForeignKey(JeuDePlateau, on_delete=models.CASCADE, null=True, blank=True, related_name='emprunts_jeu')
    date_emprunt = models.DateField(default=timezone.now().date())
    retourne = models.BooleanField(default=False)
    date_retour = models.DateField(null=True, blank=True)

    @property
    def media(self):
        if self.livre:
            return self.livre
        if self.dvd:
            return self.dvd
        if self.cd:
            return self.cd
        return None

    def save(self, *args, **kwargs):
        is_new = not self.pk
        if is_new:
            if self.media.type_media == 'Jeu':
                raise ValidationError("Les jeux de plateau ne sont pas empruntables.")
            if not self.media.disponible:
                raise ValidationError("Média non disponible.")
            if not self.emprunteur.peut_emprunter():
                raise ValidationError("Emprunteur bloqué ou limite atteinte.")
            super().save(*args, **kwargs)
            self.media.disponible = False
            self.media.save()
        else:
            super().save(*args, **kwargs)
        self.emprunteur.verifier_retards()

    def retourner(self):
        self.retourne = True
        self.date_retour = date.today()
        self.save()
        media = self.media
        if media:
            media.disponible = True
            media.save()
        self.emprunteur.verifier_retards()

    def __str__(self):
        media = self.media
        return f"{self.emprunteur.nom} emprunte {media.nom if media else 'Inconnu'}"