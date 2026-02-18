# Comparaison: HTTP Basic Auth vs JWT

## Vue d'ensemble

Ce document compare deux méthodes d'authentification implémentées dans ce repository:
- **HTTP Basic Authentication** (projets Flask et FastAPI)
- **JWT (JSON Web Tokens)** (projets Flask et FastAPI)

**4 implémentations disponibles :**
1. Flask HTTP Basic Auth (port 5000)
2. FastAPI HTTP Basic Auth (port 8000)
3. Flask JWT Auth (port 5001)
4. **FastAPI JWT Auth (port 8001)** 

---

## Tableau comparatif

| Critère | HTTP Basic Auth | JWT |
|---------|-----------------|-----|
| **Transmission** | Base64(username:password) dans chaque requête | Token signé dans Authorization header |
| **Sécurité** | Credentials envoyés à chaque fois | Token temporaire, pas de credentials |
| **Expiration** | Pas d'expiration | Expire automatiquement (configurable) |
| **État** | Sans état (stateless) | Sans état (stateless) |
| **Révocation** | Immediate (changer le mot de passe) | Nécessite une blacklist |
| **Performance** | Léger, pas de parsing | Token plus volumineux |
| **Implémentation** | Simple | Plus complexe |
| **Standard** | RFC 7617 | RFC 7519 |
| **Cas d'usage** | APIs internes, microservices | APIs publiques, SPAs, mobile apps |

---

## HTTP Basic Authentication

### Principe
```
Authorization: Basic base64(username:password)
```

### Comment ça marche
1. Client envoie `username:password` encodé en Base64
2. Serveur décode et vérifie
3. **Répète à chaque requête**

### Exemple
```bash
# Le client envoie:
Authorization: Basic ZGFuaWVsZGF0YXNjaWVudGVzdDpkYXRhc2NpZW50ZXN0

# Décodé:
danieldatascientest:datascientest
```

### Code Flask
```python
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    user = users.get(username)
    if user and check_password_hash(user['password'], password):
        return username
    return None

@app.route('/protected')
@auth.login_required
def protected():
    return {"user": auth.current_user()}
```

### Avantages
- **Simple**: Facile à implémenter
- **Léger**: Pas de token à gérer
- **Révocation immédiate**: Changer le mot de passe suffit
- **Standard**: Supporté nativement par les navigateurs

### Inconvénients
- **Sécurité**: Credentials transmis à chaque requête
- **Pas d'expiration**: Token valide tant que le mot de passe ne change pas
- **Pas de permissions fines**: Juste username/password
- **HTTPS obligatoire**: Sinon credentials en clair

### Cas d'usage
- APIs internes (microservices entre eux)
- Prototypes rapides
- Scripts automatiques
- Outils CLI

---

## JWT (JSON Web Tokens)

### Principe
```
Authorization: Bearer <header>.<payload>.<signature>
```

### Comment ça marche
1. Client envoie credentials **une fois** à `/login`
2. Serveur génère un JWT signé
3. Client utilise le token pour les requêtes suivantes
4. Token expire automatiquement

### Exemple
```bash
# 1. Login (une fois)
curl -X POST -H "Content-Type: application/json" \
  -d '{"username":"daniel", "password":"secret"}' \
  http://localhost:5001/login

# Réponse:
{"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}

# 2. Utiliser le token (toutes les requêtes suivantes)
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  http://localhost:5001/protected
```

### Structure du JWT
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9 ← HEADER (algorithme)
.
eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc3MTQxM... ← PAYLOAD (données)
.
WLkDJI3z2QTzdQTgIXoJ_lT-9hwq9BrVvclN0U... ← SIGNATURE (sécurité)
```

### Code Flask
```python
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app.config['JWT_SECRET_KEY'] = 'your-secret-key'
jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    if verify_credentials(username, password):
        access_token = create_access_token(identity=username)
        return {'access_token': access_token}
    
    return {'msg': 'Bad credentials'}, 401

@app.route('/protected')
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return {'logged_in_as': current_user}
```

### Code FastAPI 
```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
import jwt
import time

JWT_SECRET = "your-secret-key"
JWT_ALGORITHM = "HS256"

class JWTBearer(HTTPBearer):
    async def __call__(self, request):
        credentials = await super().__call__(request)
        if not self.verify_jwt(credentials.credentials):
            raise HTTPException(403, "Invalid or expired token")
        return credentials.credentials
    
    def verify_jwt(self, token: str):
        try:
            decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            return decoded["expires"] >= time.time()
        except:
            return False

@api.post("/login")
async def login(user: UserSchema):
    if verify_credentials(user.username, user.password):
        token = jwt.encode({
            "user_id": user.username,
            "expires": time.time() + 600
        }, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return {"access_token": token}
    return {"error": "Bad credentials"}, 401

@api.get("/protected", dependencies=[Depends(JWTBearer())])
async def protected():
    return {"message": "secured"}
```

### Avantages
- **Sécurité**: Credentials envoyés une seule fois
- **Expiration**: Token expire automatiquement
- **Données supplémentaires**: Peut contenir roles, permissions
- **Distribué**: Pas besoin de session serveur
- **Refresh tokens**: Peut renouveler sans re-login

### Inconvénients
- **Complexité**: Plus de code à écrire
- **Révocation difficile**: Nécessite une blacklist
- **Taille**: Token plus volumineux que Basic Auth
- **Clé secrète**: Doit être gardée sécurisée
- **Contenu lisible**: Payload en Base64 (pas chiffré)

### Cas d'usage
- APIs REST publiques
- Applications Single Page (SPA)
- Applications mobiles
- Systèmes distribués (microservices)
- OAuth2 / OpenID Connect

---

## Comparaison détaillée

### 1. Flux d'authentification

#### HTTP Basic Auth
```
Client Serveur
  | |
  |-- GET /protected ---> |
  | Basic base64(u:p) |
  | | Vérifie u:p
  |<--- 200 OK ---------- |
  | |
  |-- GET /other -------> |
  | Basic base64(u:p) | Vérifie u:p (encore)
  |<--- 200 OK ---------- |
```

#### JWT
```
Client Serveur
  | |
  |-- POST /login ------> |
  | {username, pass} | Vérifie u:p
  |<--- access_token ---- |
  | |
  |-- GET /protected ---> |
  | Bearer <token> | Vérifie signature
  |<--- 200 OK ---------- |
  | |
  |-- GET /other -------> |
  | Bearer <token> | Vérifie signature
  |<--- 200 OK ---------- |
```

### 2. Sécurité

#### HTTP Basic Auth
```
 RISQUES:
- Credentials exposés à chaque requête
- Interception = compromission totale
- Attaque par rejeu possible
- HTTPS absolument obligatoire

 AVANTAGES:
- Révocation immédiate (changer password)
- Pas de token à voler
- Simple à auditer
```

#### JWT
```
 AVANTAGES:
- Credentials envoyés 1 seule fois
- Token temporaire (expiration)
- Contenu signé (anti-falsification)
- Données supplémentaires (roles)

 RISQUES:
- Token volé = accès jusqu'à expiration
- Révocation difficile (needs blacklist)
- Secret key compromise = catastrophe
- Payload lisible (pas chiffré)
```

### 3. Performance

#### HTTP Basic Auth
```python
# Chaque requête:
1. Décoder Base64 (~1ms)
2. Chercher user en DB (~5-10ms)
3. Vérifier hash (~50-100ms avec bcrypt)
TOTAL: ~60-110ms par requête
```

#### JWT
```python
# Login (1 fois):
1. Chercher user (~5-10ms)
2. Vérifier hash (~50-100ms)
3. Créer token (~1ms)
TOTAL: ~60-110ms

# Requêtes suivantes:
1. Vérifier signature (~1ms)
2. Décoder payload (~1ms)
TOTAL: ~2ms par requête (50x plus rapide!)
```

### 4. Stockage client

#### HTTP Basic Auth
```javascript
// Navigateur: Stockage automatique
// Prompt navigateur ou stockage manuel

// JavaScript
localStorage.setItem('username', 'daniel');
localStorage.setItem('password', 'secret'); // DANGEREUX!

// Envoi
fetch('/api/data', {
  headers: {
    'Authorization': 'Basic ' + btoa(username + ':' + password)
  }
});
```

#### JWT
```javascript
// Stocker le token
localStorage.setItem('token', access_token); // Ou sessionStorage

// Envoyer
fetch('/api/data', {
  headers: {
    'Authorization': 'Bearer ' + localStorage.getItem('token')
  }
});

// Vulnérable à XSS
// Mieux: httpOnly cookie
```

---

## Architectures recommandées

### Microservices internes
```
Service A --Basic Auth--> Service B
           --Basic Auth--> Service C

 Recommandé: HTTP Basic Auth
   Pourquoi: Services se font confiance, simplicité
```

### API publique + SPA
```
Browser --JWT--> API Server
Mobile --JWT--> API Server

 Recommandé: JWT
   Pourquoi: Multi-plateforme, expiration, sécurité
```

### Système hybride
```
Admin Tool --Basic Auth--> Admin API
Mobile App --JWT--------> Public API
                             |
                             v
                        Admin API (internal)

 Best of both worlds
```

---

## Implémentation dans ce repository

### Flask HTTP Basic Auth
```bash
cd /home/ubuntu/projects/flask_http_basic_auth
source venv/bin/activate
python flask_http_basic.py
# Teste avec: python test_api.py
```

### FastAPI HTTP Basic Auth
```bash
cd /home/ubuntu/fastapi_learning/advanced
source ../../venv/bin/activate
python fastapi_http_basic.py
# Teste avec: python test_fastapi_basic.py
```

### Flask JWT
```bash
cd /home/ubuntu/projects/flask_jwt_auth
source venv/bin/activate
python flask_jwt.py
# Teste avec: python test_flask_jwt.py
```

### FastAPI JWT 
```bash
cd /home/ubuntu/fastapi_learning/advanced
source /home/ubuntu/venv/bin/activate
python3 fastapi_jwt.py
# Teste avec: python3 test_fastapi_jwt.py
# Docs: http://127.0.0.1:8001/docs
```

---

## Ressources

### HTTP Basic Auth
- [RFC 7617](https://datatracker.ietf.org/doc/html/rfc7617)
- [flask-httpauth docs](https://flask-httpauth.readthedocs.io/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)

### JWT
- [JWT.io](https://jwt.io/) - Décodeur JWT en ligne
- [RFC 7519](https://datatracker.ietf.org/doc/html/rfc7519)
- [flask-jwt-extended docs](https://flask-jwt-extended.readthedocs.io/)

---

## Quelle méthode choisir?

### Utilise HTTP Basic Auth si:
- API interne (microservices)
- Prototype rapide
- Petit nombre de requêtes
- CLI tools / scripts
- Simplicité prioritaire

### Utilise JWT si:
- API publique
- Application mobile
- Single Page Application (SPA)
- Grand nombre de requêtes
- Besoin de roles/permissions
- Architecture distribuée

### Utilise OAuth2 si:
- Authentification tierce (Google, GitHub)
- Délégation d'accès
- Scopes multiples
- Application publique avec users externes

---

## Best practices

### Pour HTTP Basic Auth:
```python
 FAIRE:
- Utiliser HTTPS en production
- Hasher les mots de passe (bcrypt, pbkdf2)
- Limiter les tentatives de connexion
- Logger les échecs d'authentification

 NE PAS FAIRE:
- Utiliser sans HTTPS
- Stocker les mots de passe en clair
- Exposer publiquement
```

### Pour JWT:
```python
 FAIRE:
- Utiliser une clé secrète forte (32+ bytes)
- Définir une expiration courte (15-30 min)
- Utiliser refresh tokens pour longue session
- Implémenter une blacklist pour logout
- Valider le token à chaque requête
- Utiliser HTTPS

 NE PAS FAIRE:
- Mettre de données sensibles dans payload
- Utiliser la même clé partout
- Token sans expiration
- Client-side validation only
- Stockage dans localStorage (préférer httpOnly cookie)
```

---

## Tests

Tous les projets incluent des tests automatisés:
- `test_api.py` (Flask Basic)
- `test_fastapi_basic.py` (FastAPI Basic)
- `test_flask_jwt.py` (Flask JWT)

Lance les tests:
```bash
python test_*.py
```

---

## Conclusion

**HTTP Basic Auth** est parfait pour la simplicité et les APIs internes.

**JWT** est le standard moderne pour les APIs publiques et applications client riches.

Le choix dépend de ton cas d'usage ! 
