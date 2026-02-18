# Flask HTTP Basic Auth - Projet d'Authentification

## Description

Ce projet démontre l'implémentation de **HTTP Basic Authentication** avec Flask. Il inclut :
- Authentification basique avec nom d'utilisateur et mot de passe
- Système de rôles (admin, user)
- Mots de passe hachés avec Werkzeug
- Plusieurs routes protégées par différents niveaux d'accès

## Concept : HTTP Basic Auth

### Processus d'authentification

1. **Client** → Envoie une requête au serveur
2. **Serveur** → Répond avec code 401 + header `WWW-Authenticate: Basic`
3. **Client** → Renvoie la requête avec header `Authorization: Basic <credentials-base64>`
4. **Serveur** → Répond avec 200 (succès) ou 403 (non autorisé)

### Encodage des credentials

Les credentials sont encodés en **Base64** au format `username:password`

**Exemple :**
```bash
# username: hello, password: world
echo -n "hello:world" | base64
# Résultat: aGVsbG86d29ybGQ=

# Header Authorization final:
# Authorization: Basic aGVsbG86d29ybGQ=
```

En Python :
```python
import base64
base64.b64encode(b"hello:world")
# b'aGVsbG86d29ybGQ='
```

## Installation

### Prérequis
- Python 3.8+
- pip

### Étapes

```bash
# 1. Activer l'environnement virtuel (si disponible)
source ~/venv/bin/activate

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer l'API
python flask_http_basic.py
```

L'API sera accessible sur : **http://0.0.0.0:5000**

## Utilisateurs disponibles

| Username | Password | Rôles | Ressource privée |
|----------|---------------|--------------|--------------------------|
| daniel | datascientest | admin, user | Private Resource Daniel |
| john | secret | user | Private Resource John |

## Routes disponibles

### 1. Route publique (index) - `/`
- **Méthode :** GET
- **Authentification :** Requise
- **Rôle requis :** `user`
- **Réponse :** Message de bienvenue avec le nom d'utilisateur

### 2. Route admin - `/admin`
- **Méthode :** GET
- **Authentification :** Requise
- **Rôle requis :** `admin`
- **Réponse :** Message confirmant le statut admin

### 3. Route privée - `/private`
- **Méthode :** GET
- **Authentification :** Requise
- **Rôle requis :** `user`
- **Réponse :** Ressource privée de l'utilisateur

## Tests

### Avec curl

```bash
# Test sans authentification (erreur 401)
curl http://localhost:5000/

# Test avec daniel (admin + user)
curl -u daniel:datascientest http://localhost:5000/
curl -u daniel:datascientest http://localhost:5000/admin
curl -u daniel:datascientest http://localhost:5000/private

# Test avec john (user seulement)
curl -u john:secret http://localhost:5000/
curl -u john:secret http://localhost:5000/private
curl -u john:secret http://localhost:5000/admin # Erreur 403 (Forbidden)

# Test avec header Authorization manuel
curl -H "Authorization: Basic ZGFuaWVsOmRhdGFzY2llbnRlc3Q=" http://localhost:5000/admin
```

### Avec Python

```python
import requests
from requests.auth import HTTPBasicAuth

# Requête authentifiée
response = requests.get(
    'http://localhost:5000/',
    auth=HTTPBasicAuth('daniel', 'datascientest')
)
print(response.text)

# Ou version courte
response = requests.get('http://localhost:5000/', auth=('daniel', 'datascientest'))
print(response.text)
```

### Avec un navigateur Web

Accédez à http://localhost:5000/ dans votre navigateur. Une boîte de dialogue s'ouvrira automatiquement pour saisir :
- **Nom d'utilisateur :** daniel ou john
- **Mot de passe :** datascientest ou secret

## Codes de statut HTTP

| Code | Signification |
|------|----------------------------------------------------|
| 200 | Succès - Authentification et autorisation OK |
| 401 | Unauthorized - Pas d'authentification |
| 403 | Forbidden - Authentifié mais pas les droits |

## Architecture du code

### Structure
```
flask_http_basic_auth/
 flask_http_basic.py # API principale
 requirements.txt # Dépendances Python
 README.md # Cette documentation
 test_api.py # Script de tests automatisés
```

### Composants clés

**1. Hashage des mots de passe**
```python
generate_password_hash("datascientest") # Créer un hash
check_password_hash(hash, "datascientest") # Vérifier
```

**2. Décorateurs Flask-HTTPAuth**
- `@auth.verify_password` : Valide les credentials
- `@auth.get_user_roles` : Récupère les rôles
- `@auth.login_required(role='...')` : Protège les routes

**3. Système de rôles**
- Les rôles peuvent être une liste `['admin', 'user']` ou une chaîne `'user'`
- Si un utilisateur a le rôle `admin`, il a automatiquement accès aux routes `user`

## Sécurité

### Limitations de Basic Auth

1. **Pas de chiffrement** : Les credentials sont juste encodés en Base64 (pas chiffrés !)
   - N'importe qui peut décoder : `echo "aGVsbG86d29ybGQ=" | base64 -d`
   - **Solution** : Toujours utiliser HTTPS en production

2. **Credentials envoyés à chaque requête**
   - Augmente le risque d'interception
   - **Alternative** : JWT, OAuth2, sessions

3. **Pas d'expiration**
   - Les credentials restent valides indéfiniment
   - **Alternative** : Tokens avec expiration

### Bonnes pratiques appliquées

- Mots de passe hachés (avec `werkzeug.security`)
- Système de rôles pour la séparation des privilèges
- Host `0.0.0.0` pour accepter les connexions externes

### Pour aller plus loin

- Ajouter HTTPS avec SSL/TLS
- Implémenter un système de tokens (JWT)
- Ajouter une base de données (SQLite, PostgreSQL)
- Implémenter OAuth2 avec Flask-Dance
- Ajouter un rate limiting

## Références

- [Flask-HTTPAuth Documentation](https://flask-httpauth.readthedocs.io/)
- [RFC 7617 - HTTP Basic Auth](https://tools.ietf.org/html/rfc7617)
- [Werkzeug Security](https://werkzeug.palletsprojects.com/en/2.3.x/utils/#module-werkzeug.security)
