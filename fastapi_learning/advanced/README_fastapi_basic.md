# FastAPI HTTP Basic Auth

## Description

Implémentation de **HTTP Basic Authentication** avec FastAPI. Ce projet démontre :
- Authentification HTTP Basic avec FastAPI Security
- Hachage des mots de passe avec passlib (pbkdf2_sha256)
- Routes protégées avec dépendances (`Depends`)
- Documentation automatique (Swagger UI et ReDoc)
- Gestion des erreurs 401 Unauthorized

## Différences FastAPI vs Flask

| Aspect | Flask (flask-httpauth) | FastAPI (fastapi.security) |
|--------|------------------------|----------------------------|
| **Décorateur** | `@auth.login_required()` | `Depends(get_current_user)` |
| **Hashage** | Werkzeug | Passlib (pbkdf2/bcrypt) |
| **Documentation** | Manuelle | Automatique (OpenAPI) |
| **Validation** | Manuelle | Automatique (Pydantic) |
| **Performance** | Sync | Async/Await supporté |

## Installation

### Prérequis
- Python 3.8+
- pip

### Étapes

```bash
# 1. Activer l'environnement virtuel
source ~/venv/bin/activate

# 2. Installer les dépendances
pip install fastapi uvicorn "passlib[bcrypt]"

# 3. Lancer l'API
cd fastapi_learning/advanced
uvicorn fastapi_http_basic:app --reload --port 8000
```

L'API sera accessible sur : **http://0.0.0.0:8000**

## Utilisateurs disponibles

| Username | Password | Hash Method |
|----------|---------------|-----------------|
| daniel | datascientest | pbkdf2_sha256 |
| john | secret | pbkdf2_sha256 |

## Routes disponibles

### 1. Route racine - `/`
- **Méthode :** GET
- **Authentification :** Non requise (publique)
- **Réponse :** Informations sur l'API et endpoints disponibles

### 2. Route utilisateur - `/user`
- **Méthode :** GET
- **Authentification :** Requise
- **Réponse :** Message de bienvenue avec username
- **Exemple :** `"Hello daniel"`

### 3. Route profil - `/me`
- **Méthode :** GET
- **Authentification :** Requise
- **Réponse :** Informations complètes de l'utilisateur (sans le hash)

### 4. Documentation interactive - `/docs`
- **Swagger UI** avec interface de test intégrée
- Bouton "Authorize" pour tester l'authentification

### 5. Documentation alternative - `/redoc`
- **ReDoc** - Documentation alternative élégante

## Tests

### Avec curl

```bash
# Test route publique
curl http://localhost:8000/

# Test sans authentification (erreur 401)
curl -X GET -i http://localhost:8000/user

# Test avec daniel
curl -u daniel:datascientest http://localhost:8000/user
curl -u daniel:datascientest http://localhost:8000/me

# Test avec john
curl -u john:secret http://localhost:8000/user

# Test avec header Authorization manuel
# daniel:datascientest en Base64 = ZGFuaWVsOmRhdGFzY2llbnRlc3Q=
curl -X GET http://localhost:8000/user \
  -H 'Authorization: Basic ZGFuaWVsOmRhdGFzY2llbnRlc3Q='

# Test avec mauvais mot de passe (erreur 401)
curl -i -u daniel:wrongpassword http://localhost:8000/user
```

### Avec Python (requests)

```python
import requests
from requests.auth import HTTPBasicAuth

BASE_URL = "http://localhost:8000"

# Route publique
response = requests.get(f"{BASE_URL}/")
print(response.json())

# Avec authentification
response = requests.get(
    f"{BASE_URL}/user",
    auth=HTTPBasicAuth('daniel', 'datascientest')
)
print(response.text) # "Hello daniel"

# Syntaxe courte
response = requests.get(f"{BASE_URL}/me", auth=('daniel', 'datascientest'))
print(response.json())
```

### Avec Swagger UI (navigateur)

1. Ouvrir http://localhost:8000/docs
2. Cliquer sur le cadenas ou le bouton "Authorize"
3. Entrer :
   - **Username:** daniel
   - **Password:** datascientest
4. Cliquer sur "Authorize"
5. Tester les endpoints directement dans l'interface

## Codes de statut HTTP

| Code | Signification | Quand |
|------|---------------|-------|
| 200 | OK | Authentification réussie |
| 401 | Unauthorized | Pas de credentials ou credentials invalides |

## Architecture du code

### Composants clés

**1. CryptContext (passlib)**
```python
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
```
- Gère le hachage et la vérification des mots de passe
- `pbkdf2_sha256` : Plus compatible que bcrypt
- Hashes pré-calculés pour éviter des problèmes au démarrage

**2. HTTPBasic (FastAPI)**
```python
security = HTTPBasic()
```
- Active l'authentification HTTP Basic
- Gère automatiquement le header `WWW-Authenticate: Basic`

**3. Fonction de vérification**
```python
def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    # Vérifie username et password
    # Lève HTTPException 401 si invalides
    return username
```

**4. Protection des routes avec Depends**
```python
@app.get("/user")
def current_user(username: str = Depends(get_current_user)):
    # Cette route nécessite une authentification
    return f"Hello {username}"
```

## Sécurité

### Bonnes pratiques appliquées

1. **Mots de passe hachés** avec passlib (pbkdf2_sha256)
   - Impossible de retrouver le mot de passe original
   - Résistant aux attaques par rainbow tables

2. **Pas de mots de passe en clair** dans le code
   - Utilisés uniquement pour générer les hashes

3. **Informations sensibles filtrées**
   - Le hash n'est jamais exposé dans l'API (`/me`)

### Limitations de Basic Auth

1. **Encodage Base64 ≠ Chiffrement**
   ```bash
   echo "ZGFuaWVsOmRhdGFzY2llbnRlc3Q=" | base64 -d
   # Résultat: daniel:datascientest
   ```
   - N'importe qui peut décoder !
   - **Solution** : Toujours utiliser HTTPS en production

2. **Credentials envoyés à chaque requête**
   - Aucun système de session/token
   - Augmente le risque d'interception

3. **Pas d'expiration**
   - Les credentials restent valides indéfiniment

### Pour aller plus loin

- [ ] Ajouter HTTPS (SSL/TLS)
- [ ] Implémenter JWT (JSON Web Tokens)
- [ ] Ajouter OAuth2 avec Password Flow
- [ ] Implémenter des rôles/permissions
- [ ] Ajouter rate limiting
- [ ] Utiliser une vraie base de données
- [ ] Logger les tentatives d'authentification

## Encodage Base64

### Comment ça fonctionne ?

```bash
# Encoder
echo -n "daniel:datascientest" | base64
# Résultat: ZGFuaWVsOmRhdGFzY2llbnRlc3Q=

echo -n "john:secret" | base64
# Résultat: am9objpzZWNyZXQ=

# Décoder (ATTENTION: C'est FACILE !)
echo "am9objpzZWNyZXQ=" | base64 -d
# Résultat: john:secret
```

```python
import base64

# Encoder
credentials = "john:secret"
encoded = base64.b64encode(credentials.encode()).decode()
print(encoded) # am9objpzZWNyZXQ=

# Décoder
decoded = base64.b64decode(encoded).decode()
print(decoded) # john:secret
```

## Comparaison Flask vs FastAPI

### Code Flask
```python
@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(...):
        return username

@app.route('/user')
@auth.login_required
def user():
    return f"Hello {auth.current_user()}"
```

### Code FastAPI
```python
def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    if not users.get(username) or not pwd_context.verify(...):
        raise HTTPException(status_code=401, ...)
    return username

@app.get("/user")
def user(username: str = Depends(get_current_user)):
    return f"Hello {username}"
```

**Avantages FastAPI :**
- Documentation automatique (Swagger/ReDoc)
- Support natif d'async/await
- Validation automatique avec Pydantic
- Injection de dépendances élégante

**Avantages Flask :**
- Plus simple pour débuter
- Écosystème mature (extensions)
- Code plus court pour les cas simples

## Références

- [FastAPI Security Documentation](https://fastapi.tiangolo.com/tutorial/security/)
- [Passlib Documentation](https://passlib.readthedocs.io/)
- [RFC 7617 - HTTP Basic Auth](https://tools.ietf.org/html/rfc7617)
- [OWASP Authentication Cheatsheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
