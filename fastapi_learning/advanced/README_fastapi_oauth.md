# FastAPI OAuth 2.0 Authentication

Implémentation d'**OAuth 2.0 (Open Authorization)** avec **FastAPI** + **JWT**.

OAuth 2.0 est le **standard moderne** pour l'authentification et l'autorisation sur le web.

## Table des matières

- [Qu'est-ce qu'OAuth 2.0 ?](#quest-ce-quoauth-20-)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Routes disponibles](#routes-disponibles)
- [Tests](#tests)
- [OAuth2 vs JWT simple](#oauth2-vs-jwt-simple)
- [Swagger UI](#swagger-ui)
- [Sécurité](#sécurité)

---

## Qu'est-ce qu'OAuth 2.0 ?

**OAuth 2.0** est un protocole d'autorisation qui permet à une application d'obtenir un accès limité à des ressources protégées **sans exposer** les identifiants de l'utilisateur.

### Composants clés

| Composant | Rôle |
|-----------|------|
| **Client** | L'application qui veut accéder aux ressources |
| **Resource Owner** | L'utilisateur qui possède les ressources |
| **Authorization Server** | Vérifie l'identité et fournit le token |
| **Resource Server** | Héberge les ressources et vérifie le token |

### Processus (6 étapes)

```
   Client Authorization Server Resource Server
     | | |
     |--1. Demande d'accès--------------->| |
     |<--2. Autorisation accordée---------| |
     |--3. Demande de token-------------->| |
     |<--4. Access token + token_type-----| |
     |--5. Requête avec token----------------------------------->|
     |<--6. Ressource protégée-------------------------------|
```

### OAuth 2.0 vs OAuth 1.0

| Aspect | OAuth 1.0 | OAuth 2.0 |
|--------|-----------|-----------|
| **Complexité** | Signature cryptographique requise | Plus simple |
| **Performance** | Plus lent | Plus rapide |
| **Flexibilité** | Un seul flux | Plusieurs flux (Password, Client Credentials, etc.) |
| **Support** | Obsolète | Standard actuel |

---

## Installation

### Prérequis

```bash
pip install fastapi uvicorn passlib pyjwt python-multipart
```

 **python-multipart** est obligatoire pour gérer les form-data OAuth2 !

### Lancer l'API

```bash
cd /home/ubuntu/fastapi_learning/advanced
source /home/ubuntu/venv/bin/activate
python3 fastapi_oauth.py
```

L'API sera accessible sur : **http://127.0.0.1:8002**

Documentation interactive :
- **Swagger UI** : http://127.0.0.1:8002/docs 
- **ReDoc** : http://127.0.0.1:8002/redoc

---

## Utilisation

### 1. Route publique

```bash
curl http://127.0.0.1:8002/
```

**Réponse :**
```json
{
  "message": "FastAPI OAuth 2.0 Authentication API",
  "endpoints": {
    "/": "Route publique",
    "/token": "Obtenir un access token (POST, form-data)",
    "/secured": "Route protégée (GET, Bearer token requis)"
  },
  "users": ["danieldatascientest", "johndatascientest"],
  "token_expiration": "30 minutes",
  "auth_type": "OAuth 2.0 Password Flow + JWT"
}
```

---

### 2. Obtenir un access token (OAuth2 Password Flow)

 **IMPORTANT** : OAuth2 utilise **form-data**, PAS JSON !

```bash
curl -X POST http://127.0.0.1:8002/token \
  -d "username=danieldatascientest" \
  -d "password=datascientest"
```

**Réponse :**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Note :** Le token expire après **30 minutes**.

---

### 3. Utiliser le token

#### Sauvegarder le token

```bash
TOKEN=$(curl -s -X POST http://127.0.0.1:8002/token \
  -d "username=danieldatascientest" \
  -d "password=datascientest" | jq -r '.access_token')
```

#### Accéder à une route protégée

```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://127.0.0.1:8002/secured
```

**Réponse :**
```json
{
  "message": "Hello World, but secured!",
  "user": {
    "username": "danieldatascientest",
    "name": "Daniel Datascientest",
    "email": "daniel@datascientest.com",
    "resource": "Module DE"
  }
}
```

---

### 4. Obtenir les informations de l'utilisateur connecté

```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://127.0.0.1:8002/me
```

**Réponse :**
```json
{
  "username": "danieldatascientest",
  "name": "Daniel Datascientest",
  "email": "daniel@datascientest.com",
  "resource": "Module DE"
}
```

---

## Routes disponibles

### POST /token (OAuth2)

Obtenir un access token via le flux OAuth2 Password.

**Body (form-data) :**
```
username=danieldatascientest
password=datascientest
```

 Ne PAS utiliser JSON, utiliser **form-data** !

**Réponse :**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

---

### GET /

Route publique, accessible sans authentification.

---

### GET /secured

Route protégée, nécessite un Bearer token.

**Headers :**
```
Authorization: Bearer <access_token>
```

---

### GET /me

Retourne les informations de l'utilisateur connecté.

**Headers :**
```
Authorization: Bearer <access_token>
```

---

## Tests

### Lancer les tests automatisés

```bash
# S'assurer que l'API est lancée
python3 fastapi_oauth.py

# Dans un autre terminal
python3 test_fastapi_oauth.py
```

### Tests inclus

Le fichier `test_fastapi_oauth.py` contient **10 tests** :

1. Accès à la route publique
2. Obtenir token via OAuth2 (form-data)
3. Token avec mauvais credentials (400)
4. Accès route sécurisée avec token valide
5. Accès route sécurisée sans token (401)
6. Accès route sécurisée avec token invalide (401)
7. Route /me (informations utilisateur)
8. Décodage et analyse JWT
9. Comparaison OAuth2 vs JWT simple
10. Démonstration form-data vs JSON

**Résultat :** **10/10 tests passés** 

---

## OAuth2 vs JWT simple

### Différences clés

| Aspect | JWT simple | OAuth 2.0 + JWT |
|--------|-----------|-----------------|
| **Route** | `POST /login` | `POST /token` |
| **Format** | JSON | **form-data** |
| **Réponse** | `{"access_token": "..."}` | `{"access_token": "...", "token_type": "bearer"}` |
| **Standard** | RFC 7519 (JWT) | RFC 6749 (OAuth 2.0) + RFC 7519 (JWT) |
| **Header** | `Authorization: Bearer <token>` | `Authorization: Bearer <token>` |
| **Use case** | APIs simples | Applications pro, multi-platform |

### Exemple comparaison

#### JWT simple (notre implémentation précédente)
```bash
# JSON
curl -X POST http://127.0.0.1:8001/user/signup \
  -H "Content-Type: application/json" \
  -d '{"username": "daniel", "password": "secret"}'

# Réponse
{"access_token": "eyJ..."}
```

#### OAuth2 (cette implémentation)
```bash
# form-data
curl -X POST http://127.0.0.1:8002/token \
  -d "username=daniel" \
  -d "password=secret"

# Réponse
{"access_token": "eyJ...", "token_type": "bearer"}
```

---

## Swagger UI

### Tester dans Swagger UI

1. **Ouvre** http://127.0.0.1:8002/docs

2. **Clique sur le cadenas ** "Authorize" (en haut à droite)

3. **Entre les credentials :**
   - Username: `danieldatascientest`
   - Password: `datascientest`
   - Client credentials: Laisse vide
   - Client ID: Laisse vide
   - Client Secret: Laisse vide

4. **Clique "Authorize"** puis **"Close"**

5. **Teste les routes protégées** (`/secured`, `/me`)

### Composants du formulaire OAuth2

| Champ | Description | Requis ? |
|-------|-------------|----------|
| **username** | Nom d'utilisateur | Oui |
| **password** | Mot de passe | Oui |
| **Client credentials location** | Où envoyer client_id/secret | Non |
| **client_id** | Identifiant de l'application | Non (optionnel) |
| **client_secret** | Secret de l'application | Non (optionnel) |

---

## Sécurité

### Bonnes pratiques implémentées

1. **Passwords hashés** : Utilise pbkdf2_sha256
2. **Token signé** : JWT avec HMAC-SHA256
3. **Expiration** : Token expire après 30 minutes
4. **Standard OAuth2** : Suit RFC 6749
5. **Vérification stricte** : Bearer token requis

### Points d'attention

#### 1. Clé secrète

```python
# MAUVAIS (en production)
SECRET_KEY = "secret"

# BON
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
# Générer avec: openssl rand -hex 32
```

#### 2. HTTPS obligatoire en production

```python
# DANGER (http)
http://api.example.com/token

# SÉCURISÉ (https)
https://api.example.com/token
```

OAuth2 transmet des credentials → **HTTPS EST OBLIGATOIRE** en production !

#### 3. Refresh tokens

Cette implémentation basique n'inclut pas de refresh tokens. Pour les ajouter :

```python
from datetime import timedelta

REFRESH_TOKEN_EXPIRATION = timedelta(days=30)

@app.post("/token")
async def login():
    access_token = create_access_token(...)
    refresh_token = create_refresh_token(...) # À implémenter
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@app.post("/refresh")
async def refresh(refresh_token: str):
    # Valider refresh token
    # Créer nouveau access token
    ...
```

#### 4. Scopes et permissions

OAuth2 supporte les **scopes** pour des permissions granulaires :

```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"read": "Read access", "write": "Write access"}
)

@app.get("/admin", dependencies=[Security(oauth2_scheme, scopes=["write"])])
async def admin_route():
    return {"message": "Admin only"}
```

---

## Comparaison complète des méthodes

Tu as maintenant **5 implémentations** d'authentification :

| Méthode | Framework | Port | Form-data | JSON | Token type | Docs auto |
|---------|-----------|------|-----------|------|------------|-----------|
| **HTTP Basic** | Flask | 5000 | | | Base64(user:pass) | |
| **HTTP Basic** | FastAPI | 8000 | | | Base64(user:pass) | |
| **JWT simple** | Flask | 5001 | | | JWT | |
| **JWT simple** | FastAPI | 8001 | | | JWT | |
| **OAuth2** | FastAPI | 8002 | | | JWT (bearer) | |

### Quelle méthode choisir ?

#### Utilise **HTTP Basic Auth** si :
- API interne (microservices)
- Prototype rapide
- Simplicité prioritaire

#### Utilise **JWT simple** si :
- API REST publique
- Single Page Application (SPA)
- Tu veux de la flexibilité

#### Utilise **OAuth 2.0** si :
- Application professionnelle
- Multi-plateforme (web + mobile + desktop)
- Interopérabilité avec d'autres services
- Standard moderne requis
- Refresh tokens nécessaires

---

## Ressources

- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [OAuth 2.0 RFC 6749](https://datatracker.ietf.org/doc/html/rfc6749)
- [JWT RFC 7519](https://datatracker.ietf.org/doc/html/rfc7519)
- [OAuth 2.0 Simplified](https://www.oauth.com/)
- [JWT.io](https://jwt.io/) - Décodeur JWT en ligne

---

## Conclusion

**OAuth 2.0** est le **standard de facto** pour l'authentification moderne.

### Avantages

- Standard reconnu internationalement
- Interopérabilité avec d'autres services
- Support natif dans FastAPI
- Documentation Swagger automatique
- Extensible (scopes, refresh tokens)

### Inconvénients

- Plus complexe que JWT simple
- Nécessite python-multipart
- Form-data (pas JSON)

**Pour débuter** : JWT simple 
**Pour la production** : OAuth 2.0 

---

## Tests rapides

```bash
# 1. Lancer l'API
python3 fastapi_oauth.py

# 2. Test complet
curl -s -X POST http://127.0.0.1:8002/token \
  -d "username=danieldatascientest" \
  -d "password=datascientest" | \
  jq -r '.access_token' | \
  xargs -I {} curl -s -H "Authorization: Bearer {}" \
  http://127.0.0.1:8002/me | jq

# 3. Swagger UI
# Ouvre: http://127.0.0.1:8002/docs
# Clique: Authorize → Entre credentials → Teste les routes
```

 **OAuth 2.0** = L'avenir de l'authentification web !
