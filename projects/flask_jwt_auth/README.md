# Flask JWT Authentication

## Description

Implémentation de **JWT (JSON Web Tokens)** avec Flask. Ce projet démontre :
- Authentification avec tokens JWT
- Tokens signés numériquement (HS256)
- Expiration automatique (30 minutes)
- Routes protégées avec `@jwt_required()`
- Hachage des mots de passe avec passlib

## Qu'est-ce qu'un JWT ?

Un **JSON Web Token** est composé de **3 parties** séparées par des points (`.`) :

```
header.payload.signature
```

### 1. Header (En-tête)
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```
Encodé en Base64 : `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9`

### 2. Payload (Données)
```json
{
  "sub": "danieldatascientest",
  "name": "Daniel",
  "iat": 1771411245,
  "exp": 1771413045
}
```
Encodé en Base64 : `eyJzdWIiOiJkYW5pZWxkYXRhc2NpZW50ZXN0Ii...`

**Claims importants :**
- `sub` (subject) : Identité de l'utilisateur
- `iat` (issued at) : Date de création du token
- `exp` (expiration) : Date d'expiration
- `jti` (JWT ID) : Identifiant unique du token

### 3. Signature
```
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret_key
)
```

**Token complet :**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkYW5pZWxkYXRhc2NpZW50ZXN0IiwiaWF0IjoxNzcxNDExMjQ1fQ.CrOVKpMYZd4NI1Q8u9Uj-Mi6QvSeOcvnJ602zqSIu5A
```

## JWT vs HTTP Basic Auth

| Aspect | HTTP Basic Auth | JWT |
|--------|----------------|-----|
| **Format** | `Basic base64(user:pass)` | `Bearer <token>` |
| **Expiration** | Aucune | 30 minutes |
| **État** | Stateless (credentials à chaque fois) | Stateless (token unique) |
| **Sécurité** | Credentials à chaque requête | Token signé |
| **Révocation** | Impossible | Possible avec blacklist |
| **Contenu** | Juste username:password | Données personnalisées (claims) |

## Installation

### Prérequis
- Python 3.8+
- pip

### Étapes

```bash
# 1. Activer l'environnement virtuel
source ~/venv/bin/activate

# 2. Installer les dépendances (versions spécifiques requises)
pip install Flask==2.2.3 Werkzeug==2.2.2 flask-jwt-extended==4.2.1 passlib

# 3. Générer votre propre clé secrète
openssl rand -hex 32

# 4. Lancer l'API
cd projects/flask_jwt_auth
python flask_jwt.py
```

L'API sera accessible sur : **http://0.0.0.0:5001**

## Utilisateurs disponibles

| Username | Password | Resource |
|----------|----------|----------|
| danieldatascientest | datascientest | Module DE |
| johndatascientest | secret | Module DS |

## Routes disponibles

### 1. Route racine - `/`
- **Méthode :** GET
- **Authentification :** Non requise
- **Réponse :** Informations sur l'API

### 2. Route login - `/login`
- **Méthode :** POST
- **Authentification :** Non requise (c'est la route d'authentification !)
- **Body :** `{"username": "...", "password": "..."}`
- **Réponse :** `{"access_token": "<jwt>"}`
- **Expiration :** 30 minutes

### 3. Route utilisateur - `/user`
- **Méthode :** GET
- **Authentification :** JWT requis
- **Header :** `Authorization: Bearer <token>`
- **Réponse :** `{"logged_in_as": "username"}`

### 4. Route ressource - `/resource`
- **Méthode :** GET
- **Authentification :** JWT requis
- **Header :** `Authorization: Bearer <token>`
- **Réponse :** `{"resource": "...", "owner": "..."}`

## Tests

### Workflow complet

```bash
# 1. Obtenir un token JWT
TOKEN=$(curl -X POST -H "Content-Type: application/json" \
  -d '{"username":"danieldatascientest", "password":"datascientest"}' \
  http://127.0.0.1:5001/login | jq -r '.access_token')

echo "Token: $TOKEN"

# 2. Utiliser le token pour accéder aux routes protégées
curl -X GET -H "Authorization: Bearer $TOKEN" http://127.0.0.1:5001/user
# Résultat: {"logged_in_as":"danieldatascientest"}

curl -X GET -H "Authorization: Bearer $TOKEN" http://127.0.0.1:5001/resource
# Résultat: {"owner":"danieldatascientest","resource":"Module DE"}

# 3. Tester sans token (erreur 401)
curl -i -X GET http://127.0.0.1:5001/user
# Résultat: HTTP/1.1 401 UNAUTHORIZED
```

### Avec Python (requests)

```python
import requests

BASE_URL = "http://127.0.0.1:5001"

# 1. S'authentifier et obtenir le token
response = requests.post(
    f"{BASE_URL}/login",
    json={"username": "danieldatascientest", "password": "datascientest"}
)
token = response.json()["access_token"]
print(f"Token: {token}")

# 2. Utiliser le token
headers = {"Authorization": f"Bearer {token}"}

response = requests.get(f"{BASE_URL}/user", headers=headers)
print(response.json()) # {"logged_in_as": "danieldatascientest"}

response = requests.get(f"{BASE_URL}/resource", headers=headers)
print(response.json()) # {"owner": "...", "resource": "Module DE"}
```

## Décoder un JWT

### En ligne
Visitez https://jwt.io et collez votre token.

 **ATTENTION** : Le contenu du JWT est **lisible** par tous ! JWT ≠ Chiffrement.

### En ligne de commande

```bash
# Extraire le payload (partie 2)
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc3MTQxMTI0NSwianRpIjoiOWU3MzE3OTktYjJmMC00MzUyLWFjNmMtODZkZjQ3MzliYjE2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImRhbmllbGRhdGFzY2llbnRlc3QiLCJuYmYiOjE3NzE0MTEyNDUsImV4cCI6MTc3MTQxMzA0NX0.CrOVKpMYZd4NI1Q8u9Uj-Mi6QvSeOcvnJ602zqSIu5A"

echo $TOKEN | cut -d'.' -f2 | base64 -d | jq
```

### Avec Python

```python
import jwt
import json

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Décoder SANS vérifier la signature (juste lire le contenu)
decoded = jwt.decode(token, options={"verify_signature": False})
print(json.dumps(decoded, indent=2))
```

## Codes de statut HTTP

| Code | Signification | Quand |
|------|---------------|-------|
| 200 | OK | Token valide et accès autorisé |
| 401 | Unauthorized | Pas de token, token expiré, ou token invalide |
| 422 | Unprocessable Entity | Token malformé ou mauvais format |

## Architecture du code

### Configuration JWT

```python
api.config["JWT_SECRET_KEY"] = "votre_cle_secrete" # openssl rand -hex 32
api.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
jwt = JWTManager(api)
```

### Créer un token

```python
from flask_jwt_extended import create_access_token

access_token = create_access_token(identity=username)
```

### Protéger une route

```python
from flask_jwt_extended import jwt_required, get_jwt_identity

@api.route("/protected", methods=["GET"])
@jwt_required() # ← Décorateur qui exige un JWT valide
def protected_route():
    current_user = get_jwt_identity()
    return jsonify(user=current_user)
```

## Sécurité

### Avantages du JWT

1. **Stateless** : Aucune session côté serveur
2. **Expiration automatique** : Le token expire après 30 minutes
3. **Signé numériquement** : Impossible de modifier sans la clé secrète
4. **Données embarquées** : Le token contient des informations (claims)

### Limitations et dangers

1. **JWT ≠ Chiffrement**
   ```bash
   # N'importe qui peut lire le contenu !
   echo "eyJ..." | base64 -d
   ```
    **Ne jamais mettre de données sensibles** dans le payload

2. **Révocation difficile**
   - Un token reste valide jusqu'à expiration
   - Même si l'utilisateur se déconnecte
   - Solution : Blacklist côté serveur

3. **Taille du token**
   - Plus gros que Basic Auth
   - Envoyé à chaque requête

4. **HTTPS obligatoire**
   - Le token peut être intercepté
   - Toujours utiliser HTTPS en production

### Bonnes pratiques

 **À FAIRE :**
- Utiliser HTTPS en production
- Définir une expiration courte (15-30 min)
- Renouveler les tokens (refresh tokens)
- Logger les tentatives d'authentification
- Stocker la clé secrète dans les variables d'environnement

 **À NE PAS FAIRE :**
- Mettre des mots de passe dans le JWT
- Utiliser une clé secrète simple (`"secret"`)
- Token sans expiration
- Stocker le token en LocalStorage (XSS attack)

## Différences avec Basic Auth

### Ce qui change :

**1. Authentification en 2 étapes**
```bash
# Basic Auth : Credentials à chaque requête
curl -u user:pass http://api.com/resource

# JWT : Une fois au login, puis token réutilisé
curl -X POST -d '{"username":"user","password":"pass"}' http://api.com/login
curl -H "Authorization: Bearer <token>" http://api.com/resource
```

**2. Format du header**
```
# Basic Auth
Authorization: Basic ZGFuaWVsOmRhdGFzY2llbnRlc3Q=

# JWT
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**3. Expiration**
- Basic Auth : Jamais
- JWT : 30 minutes (configurable)

## Pour aller plus loin

### Refresh Tokens

Ajouter un système de refresh tokens pour prolonger la session :

```python
from flask_jwt_extended import create_refresh_token

@api.route("/login", methods=["POST"])
def login():
    # ...
    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)
    return jsonify(
        access_token=access_token,
        refresh_token=refresh_token
    )

@api.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_token)
```

### Token Blacklist

Implémenter une blacklist pour révoquer des tokens :

```python
# Configuration
api.config["JWT_BLOCKLIST_ENABLED"] = True
api.config["JWT_BLOCKLIST_TOKEN_CHECKS"] = ["access", "refresh"]

# Blacklist (en production, utiliser Redis)
blocklist = set()

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in blocklist

@api.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    blocklist.add(jti)
    return jsonify(msg="Successfully logged out")
```

### Rôles et Permissions

Ajouter des rôles dans les claims :

```python
access_token = create_access_token(
    identity=username,
    additional_claims={"role": "admin"}
)

@api.route("/admin", methods=["GET"])
@jwt_required()
def admin_only():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify(msg="Admin access required"), 403
    return jsonify(msg="Welcome admin!")
```

## Références

- [Flask-JWT-Extended Documentation](https://flask-jwt-extended.readthedocs.io/)
- [JWT.io](https://jwt.io/) - Décoder et vérifier des JWT
- [RFC 7519 - JWT Standard](https://tools.ietf.org/html/rfc7519)
- [OWASP JWT Cheatsheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)

## Comparaison : Basic Auth → JWT → OAuth2

```
Sécurité croissante →

HTTP Basic Auth
  ↓ Problème : Credentials à chaque requête
JWT
  ↓ Problème : Difficile de révoquer
OAuth2 + JWT
  ↓ Solution complète pour production
```

Maintenant que vous maîtrisez JWT avec Flask, vous êtes prêt pour OAuth2 ! 
