**Description**

Application web Django pour gérer une médiathèque. Les bibliothécaires (logué) gèrent membres et médias, avec emprunts contraints (max 3 actifs, bloqué après 1 semaine retard, jeux non-empruntables). 
Public consulte les médias. Intégration API Open Library pour auto-remplissage auteur livres. Tests unitaires inclus.

**Prérequis**

Python 3.8+.
Git.

**Installation**

**1) Cloner le projet :**
git clone https://github.com/Valkyore/mediatheque-devoir.git
cd mediatheque-devoir

**2) Environnement virtuel :**
python -m venv venv
Windows : venv\Scripts\activate
Mac/Linux : source venv/bin/activate

**3) Dépendances :**
pip install -r requirements.txt

**4) Migrations BDD **
python manage.py makemigrations
python manage.py migrate

**5) Données test **
python manage.py loaddata test_data.json

**6) Superuser (biblio) **
python manage.py createsuperuser(Username : admin, Password : admin123).

**Lancement:**
python manage.py runserver

Accueil : http://127.0.0.1:8000/
Public : /membre/menu/
Biblio : /biblio/login/ (admin/admin123) → Menu gestion.

**Fonctionnalités**

Biblio (logué) : CRUD membres/médias, emprunts/rentrées (dropdown membres éligibles, validations).
Public : Consultation médias.
API : Auto-auteur livres (Open Library).
Tests : python manage.py test bibliotheque (5 tests OK).

**Notes**

BDD : SQLite (db.sqlite3).
Données test : 3 membres, 4 médias, 3 emprunts (fixtures).
Voir RAPPORT.txt pour démarche/choix.

**Projet éducatif – libre pour usage personnel.**
