# Organisation du Workspace - APIs d'Authentification

> Collection complète d'APIs d'authentification avec **Flask** et **FastAPI** 
> Méthodes: HTTP Basic Auth, JWT, OAuth 2.0 
> Tous les projets sont testés, documentés et **ready-to-deploy** 

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.2.3-green.svg)](https://flask.palletsprojects.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.129.0-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Quick Start

```bash
# Installation
git clone <votre-repo>
cd authentication-apis-learning
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Lancer OAuth 2.0 API (recommandé)
cd fastapi_learning/advanced
uvicorn fastapi_oauth:app --port 8002 --reload

# Accéder à Swagger UI
# http://127.0.0.1:8002/docs
```

**Guide complet de déploiement:** [DEPLOYMENT.md](DEPLOYMENT.md)

---

## Structure des Dossiers

```
/home/ubuntu/
 fastapi_learning/ # Apprentissage FastAPI
    basics/ # Concepts de base
       app.py # Routes, paramètres, query strings
       users_api.py # API utilisateurs GET simple
   
    intermediate/ # Niveau intermédiaire
       exercice.py # CRUD complet (POST, PUT, DELETE)
       documentation.py # Métadonnées API
       tags_api.py # Organisation avec tags
       users_documented.py # API complètement documentée
   
    advanced/ # Concepts avancés
       errors_api.py # Gestion d'erreurs personnalisée
       fastapi_async.py # Async/await et performance
       test_requests.py # Tests de performance
      
       fastapi_http_basic.py # HTTP Basic Auth avec FastAPI
       test_fastapi_basic.py # Tests automatisés
       curl_commands_fastapi.sh # Commandes curl
       compare_flask_fastapi.py # Comparaison Flask vs FastAPI
       README_fastapi_basic.md # Documentation complète
      
       fastapi_jwt.py # JWT Authentication (port 8001)
       test_fastapi_jwt.py # Tests JWT (10 tests)
       curl_commands_jwt.sh # Commandes curl JWT
       README_fastapi_jwt.md # Documentation JWT complète
      
       fastapi_oauth.py # OAuth 2.0 Auth (port 8002)
       test_fastapi_oauth.py # Tests OAuth2 (10 tests)
       README_fastapi_oauth.md # Documentation OAuth2 complète
   
    exam/ # Examen FastAPI
       fastapi_exam_souelmi/ # Projet d'examen complet
          main.py # API Quiz avec authentification
          questions.csv # Base de données (76 questions)
          requirements.txt
          requests.txt # Exemples de requêtes curl
       main.py # Fichier main de test
   
    notebooks/ # Jupyter Notebooks
        securite_api.ipynb # Cours sécurité API

 projects/ # Projets personnels
    neo4j_metro/ # Projet Metro Paris Neo4j
   
    flask_http_basic_auth/ # Authentification HTTP Basic avec Flask
       flask_http_basic.py # API principale
       test_api.py # Tests automatisés
       curl_commands.sh # Tests curl
       requirements.txt # Dépendances
       README.md # Documentation détaillée
   
    flask_jwt_auth/ # Authentification JWT avec Flask
       flask_jwt.py # API JWT (port 5001)
       test_flask_jwt.py # Suite de tests complète (8 tests)
       curl_commands.sh # Commandes curl exemples
       start_api.sh # Script de démarrage automatique
       requirements.txt # Dépendances (Flask-JWT-Extended)
       venv/ # Environnement virtuel
       README.md # Documentation complète JWT
   
    COMPARISON_AUTH_METHODS.md # Comparaison HTTP Basic vs JWT

 archives/ # Archives et anciennes versions
    fastapi_exam.zip
    fastapi_exam_souelmi.zip
    fastapi_exam_/

 venv/ # Environnement virtuel Python
```

## Utilisation

### Lancer un serveur FastAPI

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Lancer un fichier spécifique (exemple: basics)
cd fastapi_learning/basics
uvicorn app:app --reload

# Lancer l'examen
cd fastapi_learning/exam/fastapi_exam_souelmi
uvicorn main:app --reload
```

### Accéder à la documentation

Une fois le serveur lancé :
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

### Lancer un serveur Flask

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Lancer le projet Flask HTTP Basic Auth
cd projects/flask_http_basic_auth
python flask_http_basic.py
# API accessible sur: http://localhost:5000

# Lancer le projet Flask JWT Auth 
cd projects/flask_jwt_auth
./start_api.sh
# Ou manuellement:
# source venv/bin/activate && python flask_jwt.py
# API accessible sur: http://localhost:5001

# Lancer le projet FastAPI JWT Auth 
cd fastapi_learning/advanced
python3 fastapi_jwt.py
# API accessible sur: http://localhost:8001
# Docs: http://localhost:8001/docs

# Lancer le projet FastAPI OAuth 2.0 Auth 
cd fastapi_learning/advanced
python3 fastapi_oauth.py
# API accessible sur: http://localhost:8002
# Docs: http://localhost:8002/docs
```

### Tester les APIs d'authentification

```bash
# HTTP Basic Auth (Flask)
cd projects/flask_http_basic_auth
python test_api.py

# HTTP Basic Auth (FastAPI)
cd fastapi_learning/advanced
python test_fastapi_basic.py

# JWT Auth (Flask) 
cd projects/flask_jwt_auth
python test_flask_jwt.py

# JWT Auth (FastAPI) 
cd fastapi_learning/advanced
python test_fastapi_jwt.py

# OAuth 2.0 Auth (FastAPI) 
cd fastapi_learning/advanced
python test_fastapi_oauth.py

# Consulter le document de comparaison
cat projects/COMPARISON_AUTH_METHODS.md
```

### Jupyter Notebook

```bash
# Lancer Jupyter
jupyter notebook fastapi_learning/notebooks/securite_api.ipynb
```

## Contenu par Niveau

### Basics
- Routes GET simples
- Paramètres de path et query
- Type hints et validation
- Headers HTTP

### Intermediate
- CRUD complet (POST, PUT, DELETE)
- Documentation API (métadonnées, tags)
- Pydantic models
- Organisation du code

### Advanced 
- Gestion d'erreurs (status codes 400, 404, 500)
- Async/await et performance
- Tests de charge
- Comparaison sync vs async
- **HTTP Basic Auth** avec FastAPI
- Hachage mots de passe (passlib)
- Documentation interactive (Swagger UI)
- Dépendances (`Depends`) pour auth
- Comparaison Flask vs FastAPI

### Exam
- API Quiz avec 3 endpoints
- Authentification Basic Auth
- Lecture CSV (76 questions)
- Filtrage par catégorie/type
- Autorisation admin

## Projets Flask

### Flask HTTP Basic Auth
- Authentification HTTP Basic (RFC 7617)
- Encodage Base64 des credentials
- Système de rôles (admin, user)
- Mots de passe hachés avec Werkzeug
- 3 routes protégées : /, /admin, /private
- Tests automatisés avec curl et Python
- Documentation complète avec exemples

**Utilisateurs disponibles :**
- daniel / datascientest (admin + user)
- john / secret (user)

**Endpoints :**
- `GET /` - Route accessible aux users
- `GET /admin` - Route réservée aux admins
- `GET /private` - Ressources privées des users

### Flask JWT Auth 
- Authentification par **JWT (JSON Web Tokens)** (RFC 7519)
- Token signé avec **HS256** (clé secrète 256-bit)
- Expiration automatique (30 minutes configurable)
- Décorateur `@jwt_required()` pour protection
- Hachage mots de passe avec **passlib** (pbkdf2_sha256)
- **Port 5001** (pour coexister avec Basic Auth sur 5000)
- 8 tests automatisés avec décodage JWT
- Script de démarrage automatique `./start_api.sh`

**Utilisateurs disponibles :**
- danieldatascientest / datascientest
- johndatascientest / secret

**Endpoints :**
- `GET /` - Route publique (informations API)
- `POST /login` - Obtenir un token JWT
- `GET /user` - Route protégée (retourne l'utilisateur)
- `GET /resource` - Route protégée (retourne la ressource)

**Structure du JWT :**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9 ← Header (algorithme)
.
eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc3MS4 ← Payload (données)
.
WLkDJI3z2QTzdQTgIXoJ_lT-9hwq9BrVv. ← Signature (sécurité)
```

**Tester :**
```bash
# 1. Login
TOKEN=$(curl -s -X POST -H "Content-Type: application/json" \
  -d '{"username":"danieldatascientest", "password":"datascientest"}' \
  http://127.0.0.1:5001/login | jq -r '.access_token')

# 2. Utiliser le token
curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:5001/user
```

### FastAPI JWT Auth 
- Authentification par **JWT (JSON Web Tokens)** avec FastAPI
- Token signé avec **HS256** (clé secrète 256-bit)
- Expiration automatique (10 minutes configurable)
- **Async** pour haute performance
- Classe custom `JWTBearer` avec `dependencies=[Depends()]`
- **Port 8001** (pour coexister avec autres APIs)
- 10 tests automatisés (9/10 passés )
- Documentation **Swagger** auto-générée

**Utilisateurs disponibles :**
- Inscription via `/user/signup`
- Connexion via `/user/login`

**Endpoints :**
- `GET /` - Route publique (informations API)
- `POST /user/signup` - Inscription (retourne token)
- `POST /user/login` - Connexion (retourne token)
- `GET /secured` - Route protégée (nécessite token)

**Tester :**
```bash
# 1. Signup
TOKEN=$(curl -s -X POST -H "Content-Type: application/json" \
  -d '{"username":"daniel", "password":"datascientest"}' \
  http://127.0.0.1:8001/user/signup | jq -r '.access_token')

# 2. Utiliser le token
curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:8001/secured

# 3. Documentation interactive
# Ouvrir: http://127.0.0.1:8001/docs
```

### FastAPI OAuth 2.0 Auth 
- Authentification **OAuth 2.0** (protocole standard moderne)
- **Password Flow** : username + password → access token
- Token JWT signé avec **HS256**
- Expiration automatique (30 minutes configurable)
- **form-data** (pas JSON) pour `/token` - Standard OAuth2
- **Async** pour haute performance
- `OAuth2PasswordBearer` + `OAuth2PasswordRequestForm`
- **Port 8002** (pour coexister avec autres APIs)
- 10 tests automatisés (10/10 passés )
- Documentation **Swagger** avec bouton "Authorize"

**Utilisateurs disponibles :**
- danieldatascientest / datascientest
- johndatascientest / secret

**Endpoints :**
- `GET /` - Route publique (informations API)
- `POST /token` - Obtenir access token OAuth2 (**form-data**)
- `GET /secured` - Route protégée (nécessite Bearer token)
- `GET /me` - Informations utilisateur connecté

**Tester :**
```bash
# 1. Obtenir token (form-data, pas JSON!)
TOKEN=$(curl -s -X POST http://127.0.0.1:8002/token \
  -d "username=danieldatascientest" \
  -d "password=datascientest" | jq -r '.access_token')

# 2. Utiliser le token
curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:8002/secured

# 3. Documentation Swagger avec Authorize
# Ouvrir: http://127.0.0.1:8002/docs
# Cliquer sur: Authorize → Entrer credentials
```

** Différence clé OAuth2 vs JWT :**
- **JWT simple** : Envoie JSON → Reçoit `{"access_token": "..."}`
- **OAuth 2.0** : Envoie form-data → Reçoit `{"access_token": "...", "token_type": "bearer"}`

OAuth 2.0 est le **standard recommandé** pour les applications professionnelles !

### Comparaison des méthodes d'authentification

Voir le document complet : [COMPARISON_AUTH_METHODS.md](projects/COMPARISON_AUTH_METHODS.md)

| Méthode | Framework | Port | Sécurité | Simplicité | Performance | Docs | Standard |
|---------|-----------|------|----------|------------|-------------|------|----------|
| **HTTP Basic** | Flask | 5000 | Credentials à chaque fois | Simple | Rapide | Manuel | RFC 7617 |
| **HTTP Basic** | FastAPI | 8000 | Credentials à chaque fois | Simple | Très rapide | Auto | RFC 7617 |
| **JWT** | Flask | 5001 | Token temporaire | Complexe | Rapide | Manuel | RFC 7519 |
| **JWT** | FastAPI | 8001 | Token temporaire | Complexe | Très rapide | Auto | RFC 7519 |
| **OAuth 2.0** | FastAPI | 8002 | Standard moderne | Plus complexe | Très rapide | Auto | RFC 6749 |

** OAuth 2.0** est le standard de facto pour les applications modernes !

## Credentials (Exam FastAPI)

**Utilisateurs:**
- alice / wonderland
- bob / builder
- clementine / mandarine

**Admin:**
- admin / 4dm1N

## Notes

- Tous les fichiers d'exercice sont séparés pour faciliter la révision
- L'examen est complet et testé avec curl
- Le notebook de sécurité couvre: authentification, autorisation, traçabilité
- Les archives contiennent les anciennes versions pour référence

---

## Déploiement

### Initialisation Git & GitHub

```bash
# 1. Utiliser le script automatique
./init_github_repo.sh

# 2. Ou manuellement
git init
git add .
git commit -m "Initial commit: Authentication APIs"

# 3. Créer repo sur GitHub puis:
git remote add origin https://github.com/VOTRE_USERNAME/NOM_REPO.git
git branch -M main
git push -u origin main
```

### Plateformes de Déploiement

| Plateforme | Gratuit | Simplicité | Recommandé pour |
|------------|---------|------------|-----------------|
| **Heroku** | 550h/mois | | Débutants |
| **Render** | 750h/mois | | Production |
| **Railway** | $5 crédit | | Développeurs |

** Guide complet avec tutoriels pas-à-pas :** 
 [DEPLOYMENT.md](DEPLOYMENT.md)

### Fichiers de Déploiement

- `requirements.txt` - Toutes les dépendances
- `Procfile` - Configuration Heroku
- `runtime.txt` - Version Python
- `.gitignore` - Fichiers à exclure
- `DEPLOYMENT.md` - Guide complet

### Variables d'Environnement Requises

```bash
SECRET_KEY=votre-secret-key-securisee
JWT_SECRET_KEY=autre-secret-jwt-different
ENVIRONMENT=production
```

**Générer des secrets sécurisés :**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## Documentation Complète

- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Guide de déploiement (Heroku, Render, Railway)
- **[COMPARISON_AUTH_METHODS.md](projects/COMPARISON_AUTH_METHODS.md)** - Comparaison HTTP Basic vs JWT
- **[COMPARISON_FLASK_FASTAPI_JWT.md](projects/COMPARISON_FLASK_FASTAPI_JWT.md)** - Flask vs FastAPI pour JWT
- **[README_fastapi_oauth.md](fastapi_learning/advanced/README_fastapi_oauth.md)** - Guide complet OAuth 2.0

---

## License

MIT License - Utilisable librement pour apprentissage et projets personnels.

---

## Contribution

Ce projet est à but pédagogique. N'hésitez pas à :
- Ouvrir des issues pour des questions
- Proposer des améliorations
- Partager vos retours d'expérience

---

## Si ce projet vous aide dans votre apprentissage, donnez-lui une étoile !

**Bon apprentissage ! **
