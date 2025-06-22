# HBnB - API avec Flask

Ce projet est une API RESTful pour la gestion d’annonces de logements (type AirBnB), développée dans le cadre de Holberton School.  
L’API permet de gérer les utilisateurs, logements, commodités et avis, avec validation métier stricte et tests automatisés.

---


## Objectif

Créer une API complète pour gérer :
- Les **utilisateurs** (User)
- Les **logements** (Place)
- Les **commodités** (Amenity)
- Les **avis** (Review)

Avec :
- Validation stricte des données
- Documentation Swagger automatique
- Tests unitaires et fonctionnels
- Architecture claire et évolutive

---

## La structure du projet
```
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── facade.py
│   ├── persistence/
│       ├── __init__.py
│       ├── repository.py
├── run.py
├── config.py
├── requirements.txt
├── README.md
```

---

## Fonctionnalités principales

- **CRUD complet** sur User, Place, Amenity, Review
- **Validation métier** : email, coordonnées, prix, unicité, etc.
- **Gestion des relations** : un utilisateur possède des logements, un logement a des commodités et des avis, etc.
- **Endpoints RESTful** clairs et versionnés (`/api/v1/`)
- **Documentation Swagger** générée automatiquement (flask-restx)
- **Tests automatisés** (pytest/unittest) et manuels (cURL/Postman)
- **Architecture scalable** : séparation claire entre API, logique métier, persistance et tests

---

## Exemples d’endpoints

| Méthode | Endpoint                                 | Description                        |
|---------|------------------------------------------|------------------------------------|
| POST    | `/api/v1/users/`                         | Créer un utilisateur               |
| GET     | `/api/v1/users/`                         | Lister tous les utilisateurs       |
| GET     | `/api/v1/users/<user_id>`                | Détail d’un utilisateur            |
| PUT     | `/api/v1/users/<user_id>`                | Modifier un utilisateur            |
| POST    | `/api/v1/places/`                        | Créer un logement                  |
| GET     | `/api/v1/places/`                        | Lister tous les logements          |
| GET     | `/api/v1/places/<place_id>`              | Détail d’un logement               |
| PUT     | `/api/v1/places/<place_id>`              | Modifier un logement               |
| POST    | `/api/v1/amenities/`                     | Créer une commodité                |
| GET     | `/api/v1/amenities/`                     | Lister toutes les commodités       |
| GET     | `/api/v1/amenities/<amenity_id>`         | Détail d’une commodité             |
| PUT     | `/api/v1/amenities/<amenity_id>`         | Modifier une commodité             |
| POST    | `/api/v1/reviews/`                       | Créer un avis                      |
| GET     | `/api/v1/reviews/`                       | Lister tous les avis               |
| GET     | `/api/v1/reviews/<review_id>`            | Détail d’un avis                   |
| PUT     | `/api/v1/reviews/<review_id>`            | Modifier un avis                   |
| DELETE  | `/api/v1/reviews/<review_id>`            | Supprimer un avis                  |

---

## Validation métier

- **User** : email valide, prénom/nom non vides
- **Place** : titre non vide, prix positif, latitude/longitude dans les bornes
- **Review** : texte non vide, rating entre 1 et 5, user/place existants
- **Amenity** : nom non vide, max 50 caractères

---

---

## Installation

1. Clone le dépôt :
   ```bash
   git clone https://github.com/yourusername/holbertonschool-hbnb.git
   cd holbertonschool-hbnb/part2/hbnb
   ```
2. Installer les dépendances nécessaires:
```bash
pip install -r requirements.txt
```

## Lancer l’application

```bash
python3 run.py
```
L'API est disponible à l'adresse 'http://127.0.0.1:5000'.

# Authors
Wassef Abdallah

Julien Girardey

Lucas Boyadjian
