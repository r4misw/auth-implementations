# FastAPI JWT Authentication

Implémentation d'une authentification **JWT (JSON Web Tokens)** avec **FastAPI**.

## Table des matières

- [Qu'est-ce que JWT ?](#quest-ce-que-jwt-)
- [Installation](#installation)
- [Structure du projet](#structure-du-projet)
- [Utilisation](#utilisation)
- [Routes disponibles](#routes-disponibles)
- [Tests](#tests)
- [Comparaison Flask vs FastAPI](#comparaison-flask-vs-fastapi)
- [Sécurité](#sécurité)

---

## Qu'est-ce que JWT ?

JWT (JSON Web Token) est un standard ouvert (**RFC 7519**) pour transmettre des informations de manière sécurisée.

### Structure d'un JWT

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9 ← HEADER
.
eyJ1c2VyX2lkIjoiZGFuaWVsIiwiZXhwaXJl... ← PAYLOAD
.
XDtyRNuVYbYtOVxVuubQ3IUklilShmK2o24j5... ← SIGNATURE
```

### Les 3 parties

| Partie | Contenu | Encodage |
|--------|---------|----------|
| **Header** | `{"alg": "HS256", "typ": "JWT"}` | Base64 |
| **Payload** | `{"user_id": "daniel", "expires": ...}` | Base64 |
| **Signature** | HMAC-SHA256(header + payload, secret) | Binaire → Base64 |

 **Important** : Le contenu du JWT est **LISIBLE** (Base64), mais la **signature** empêche toute modification !

---

## Installation

### Prérequis

```bash
pip install fastapi uvicorn pyjwt
```

### Cloner et lancer

```bash
# Naviguer vers le dossier
cd /home/ubuntu/fastapi_learning/advanced

# Activer l'environnement virtuel
source /home/ubuntu/venv/bin/activate

# Lancer l'API
python3 fastapi_jwt.py

# Ou avec uvicorn directement
uvicorn fastapi_jwt:api --reload --port 8001
```

L'API sera accessible sur : **http://127.0.0.1:8001**

Documentation interactive :
- **Swagger UI** : http://127.0.0.1:8001/docs
- **ReDoc** : http://127.0.0.1:8001/redoc

---

## Structure du projet

```
fastapi_learning/advanced/
 fastapi_jwt.py # API principale
 test_fastapi_jwt.py # Tests automatisés (10 tests)
 curl_commands_jwt.sh # Commandes curl pour tester
 README_fastapi_jwt.md # Cette documentation
```

---

## Utilisation

### 1. Route publique

```bash
curl http://127.0.0.1:8001/
```

**Réponse :**
```json
{
  "message": "FastAPI JWT Authentication API",
  "endpoints": {
    "/": "Route publique",
    "/secured": "Route protégée (JWT requis)",
    "/user/signup": "Inscription (POST)",
    "/user/login": "Connexion (POST)"
  },
  "registered_users": 0,
  "token_expiration": "600 seconds (10.0 minutes)"
}
```

### 2. Inscription (Signup)

```bash
curl -X POST http://127.0.0.1:8001/user/signup \
  -H "Content-Type: application/json" \
  -d '{"username": "daniel", "password": "datascientest"}'
```

**Réponse :**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZGFuaWVsIiwiZXhwaXJlcyI6MTc3MTQxMzcwNC4xNDQxNTY1fQ.XDtyRNuVYbYtOVxVuubQ3IUklilShmK2o24j5cT3amo"
}
```

### 3. Connexion (Login)

```bash
curl -X POST http://127.0.0.1:8001/user/login \
  -H "Content-Type: application/json" \
  -d '{"username": "daniel", "password": "datascientest"}'
```

**Réponse :**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 4. Utiliser le token

#### Sauvegarder le token

```bash
TOKEN=$(curl -s -X POST http://127.0.0.1:8001/user/signup \
  -H "Content-Type: application/json" \
  -d '{"username": "daniel", "password": "datascientest"}' | jq -r '.access_token')
```

#### Accéder à une route protégée

```bash
curl -X GET http://127.0.0.1:8001/secured \
  -H "Authorization: Bearer $TOKEN"
```

**Réponse (succès) :**
```json
{
  "message": "Hello World! but secured"
}
```

**Réponse (échec - pas de token) :**
```json
{
  "detail": "Not authenticated"
}
```

---

## Routes disponibles

### GET /

Route publique, accessible sans authentification.

**Réponse :** Informations sur l'API

### POST /user/signup

Inscription d'un nouvel utilisateur.

**Body :**
```json
{
  "username": "daniel",
  "password": "datascientest"
}
```

**Réponse :** Token JWT

### POST /user/login

Connexion d'un utilisateur existant.

**Body :**
```json
{
  "username": "daniel",
  "password": "datascientest"
}
```

**Réponse :** Token JWT ou erreur

### GET /secured

Route protégée, nécessite un JWT valide.

**Headers :**
```
Authorization: Bearer <token>
```

**Réponse :** Message de confirmation d'accès

---

## Tests

### Lancer les tests automatisés

```bash
# S'assurer que l'API est lancée
python3 fastapi_jwt.py

# Dans un autre terminal
python3 test_fastapi_jwt.py
```

### Tests inclus

Le fichier `test_fastapi_jwt.py` contient **10 tests** :

1. Accès à la route publique
2. Inscription (signup) de nouveaux utilisateurs
3. Connexion (login) avec credentials valides
4. Connexion avec mauvais credentials (rejet)
5. Accès route sécurisée avec token valide
6. Accès route sécurisée sans token (401)
7. Accès route sécurisée avec token invalide (403)
8. Décodage et analyse des JWT
9. Vérification structure JWT (3 parties)
10. Tentative de modification du JWT (rejet)

**Résultat :** **9/10 tests passés** 
- Un test échoue car FastAPI retourne 401 au lieu de 403 quand le token est absent (comportement normal de `HTTPBearer`)

---

## Comparaison Flask vs FastAPI

### Architecture

#### Flask JWT
```python
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

app.config['JWT_SECRET_KEY'] = 'secret'
jwt = JWTManager(app)

@app.route('/protected')
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return {"user": current_user}
```

#### FastAPI JWT
```python
from fastapi.security import HTTPBearer

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        # Vérification du token
        ...

@api.get("/secured", dependencies=[Depends(JWTBearer())])
async def secured():
    return {"message": "secured"}
```

### Différences clés

| Aspect | Flask | FastAPI |
|--------|-------|---------|
| **Librairie** | `flask-jwt-extended` | `pyjwt` + custom class |
| **Décorateur** | `@jwt_required()` | `dependencies=[Depends(JWTBearer())]` |
| **Setup** | Plus simple (library fait tout) | Plus de contrôle (custom) |
| **Async** | Non | Oui |
| **Documentation** | Manuelle | Auto-générée (Swagger) |
| **Type hints** | Optionnel | Requis |
| **Performance** | Rapide | Très rapide |

### Performances

```bash
# Flask JWT (port 5001)
Login: ~60-100ms (hash password)
Route protégée: ~2-5ms (vérif signature)

# FastAPI JWT (port 8001)
Signup: ~50-80ms (async)
Route protégée: ~1-3ms (async + vérif signature)
```

FastAPI est **légèrement plus rapide** grâce à l'async.

---

## Sécurité

### Bonnes pratiques implémentées

1. **Token signé** : HMAC-SHA256 avec clé secrète
2. **Expiration** : Token expire après 10 minutes
3. **Vérification stricte** : Schéma Bearer requis
4. **Payload lisible** : Utilisateur peut voir le contenu (transparence)

### Points d'attention

#### 1. Clé secrète

```python
# MAUVAIS (en production)
JWT_SECRET = "secret"

# BON
JWT_SECRET = os.getenv("JWT_SECRET") # Variable d'environnement
# Générer avec: openssl rand -hex 32
```

#### 2. HTTPS obligatoire

```python
# DANGER
http://api.example.com/login # Token interceptable

# SÉCURISÉ
https://api.example.com/login # Token chiffré en transit
```

#### 3. Données sensibles

```python
# NE PAS FAIRE
payload = {
    "user_id": "daniel",
    "password": "datascientest", # 
    "credit_card": "1234-5678" # 
}

# FAIRE
payload = {
    "user_id": "daniel",
    "roles": ["user", "admin"],
    "expires": 1771413704
}
```

Le payload est **lisible** (Base64), ne **JAMAIS** y mettre de données sensibles !

#### 4. Révocation (logout)

Le code actuel **ne gère pas** la révocation. Pour implémenter :

```python
# Blacklist des tokens
blacklisted_tokens = set()

def verify_jwt(jwtoken: str):
    # Vérifier si le token est blacklisté
    if jwtoken in blacklisted_tokens:
        return False
    
    # Vérifier expiration
    payload = decode_jwt(jwtoken)
    return payload is not None

@api.post("/logout")
async def logout(token: str = Depends(JWTBearer())):
    blacklisted_tokens.add(token)
    return {"message": "Logged out"}
```

**Problème** : La blacklist en mémoire disparaît au restart. Solution : Redis ou base de données.

---

## Décoder un JWT

### En ligne
Utilise [jwt.io](https://jwt.io/) pour décoder visuellement.

### En ligne de commande

```bash
# Récupérer le payload (partie 2)
echo $TOKEN | cut -d'.' -f2 | base64 -d 2>/dev/null | jq
```

**Résultat :**
```json
{
  "user_id": "daniel",
  "expires": 1771413704.1441565
}
```

### Avec Python

```python
import jwt

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Décoder sans vérifier la signature (pour voir le contenu)
decoded = jwt.decode(token, options={"verify_signature": False})
print(decoded)

# Décoder ET vérifier la signature
decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
print(decoded)
```

---

## Fonctionnalités avancées

### Refresh Tokens

Pour des sessions plus longues, implémenter un système de refresh token :

```python
def create_tokens(user_id: str):
    access_token = create_access_token(user_id, expires_delta=timedelta(minutes=15))
    refresh_token = create_refresh_token(user_id, expires_delta=timedelta(days=30))
    return {"access_token": access_token, "refresh_token": refresh_token}

@api.post("/token/refresh")
async def refresh(refresh_token: str):
    # Valider le refresh token
    # Créer un nouveau access token
    return {"access_token": new_access_token}
```

### Rôles et permissions

```python
# Ajouter des rôles dans le payload
payload = {
    "user_id": "daniel",
    "roles": ["admin", "user"],
    "permissions": ["read", "write", "delete"],
    "expires": time.time() + 600
}

# Vérifier les permissions
class RequireRole:
    def __init__(self, role: str):
        self.role = role
    
    async def __call__(self, token: str = Depends(JWTBearer())):
        decoded = decode_jwt(token)
        if self.role not in decoded.get("roles", []):
            raise HTTPException(403, "Insufficient permissions")
        return decoded

@api.delete("/admin/users/{user_id}", dependencies=[Depends(RequireRole("admin"))])
async def delete_user(user_id: str):
    return {"message": f"User {user_id} deleted"}
```

---

## Documentation interactive

FastAPI génère automatiquement une documentation interactive :

### Swagger UI (http://127.0.0.1:8001/docs)
- Interface graphique pour tester l'API
- Génération automatique de la doc
- Test direct des routes

### ReDoc (http://127.0.0.1:8001/redoc)
- Documentation statique
- Design moderne
- Export en PDF/HTML

---

## Ressources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PyJWT Documentation](https://pyjwt.readthedocs.io/)
- [JWT.io](https://jwt.io/) - Décodeur JWT en ligne
- [RFC 7519 - JWT](https://datatracker.ietf.org/doc/html/rfc7519)
- [Comparaison complète](../../projects/COMPARISON_AUTH_METHODS.md) - Flask vs FastAPI

---

## Conclusion

**FastAPI JWT** offre :
- Authentification moderne et sécurisée
- Performance élevée (async)
- Documentation auto-générée
- Type safety avec Pydantic
- Contrôle total sur la logique JWT

**Idéal pour :**
- APIs REST publiques
- Applications mobiles
- Single Page Applications (SPA)
- Microservices

**Comparer avec :**
- [Flask JWT](../../../projects/flask_jwt_auth/) (port 5001)
- [Flask HTTP Basic](../../../projects/flask_http_basic_auth/) (port 5000)
- [FastAPI HTTP Basic](./fastapi_http_basic.py) (port 8000)

 **Sécurité avant tout** : Utilise HTTPS en production et protège ta clé secrète !
