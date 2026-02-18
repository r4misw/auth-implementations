# Quick Start Guide

Démarrage rapide en 5 minutes ! Testez les APIs d'authentification localement.

---

## Installation

```bash
# 1. Cloner le repository
git clone <url-du-repo>
cd authentication-apis-learning

# 2. Créer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate # Linux/macOS
# ou: venv\Scripts\activate # Windows

# 3. Installer les dépendances
pip install -r requirements.txt
```

---

## Tester les APIs

### Option 1: OAuth 2.0 (Recommandé) 

```bash
# Démarrer l'API
cd fastapi_learning/advanced
uvicorn fastapi_oauth:app --port 8002 --reload

# Dans votre navigateur: http://127.0.0.1:8002/docs
# Cliquez "Authorize" → danieldatascientest / datascientest
```

** Interface Swagger UI avec authentification OAuth2 complète !**

---

### Option 2: JWT FastAPI

```bash
cd fastapi_learning/advanced
uvicorn fastapi_jwt:app --port 8001 --reload

# Tester: http://127.0.0.1:8001/docs
```

---

### Option 3: HTTP Basic Auth (Flask)

```bash
cd projects/flask_http_basic_auth
python3 flask_http_basic.py

# Tester: http://127.0.0.1:5000
```

---

## Lancer les Tests

```bash
# Tests OAuth 2.0 (10 tests)
cd fastapi_learning/advanced
python3 test_fastapi_oauth.py

# Tests JWT (10 tests)
python3 test_fastapi_jwt.py

# Tests HTTP Basic Auth
cd ../../projects/flask_http_basic_auth
python3 test_api.py
```

---

## Documentation

| Fichier | Description |
|---------|-------------|
| [README.md](README.md) | Documentation complète du projet |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Guide de déploiement (Heroku, Render, Railway) |
| [fastapi_learning/advanced/README_fastapi_oauth.md](fastapi_learning/advanced/README_fastapi_oauth.md) | OAuth 2.0 en détail |
| [projects/COMPARISON_AUTH_METHODS.md](projects/COMPARISON_AUTH_METHODS.md) | Comparaison des méthodes |

---

## Credentials de Test

**Utilisateurs disponibles (OAuth2 & JWT):**
- Username: `danieldatascientest` / Password: `datascientest`
- Username: `johndatascientest` / Password: `secret`

**HTTP Basic Auth:**
- Username: `daniel` / Password: `datascientest`

---

## Structure d'Apprentissage

**Progression recommandée:**

1. **HTTP Basic Auth** (Flask) → Comprendre les bases
2. **HTTP Basic Auth** (FastAPI) → Voir la différence de framework
3. **JWT** (Flask puis FastAPI) → Tokens et stateless auth
4. **OAuth 2.0** (FastAPI) → Standard moderne professionnel

---

## Déploiement Rapide

```bash
# 1. Initialiser Git
./init_github_repo.sh

# 2. Créer repo sur GitHub
# https://github.com/new

# 3. Push
git remote add origin <url-du-repo>
git push -u origin main

# 4. Déployer (voir DEPLOYMENT.md)
```

---

## Aide Rapide

**API ne démarre pas ?**
```bash
# Vérifier que le venv est activé
which python3
# Doit montrer: .../venv/bin/python3

# Réinstaller les dépendances
pip install -r requirements.txt
```

**Port déjà utilisé ?**
```bash
# Trouver le processus
lsof -i :8002 # Remplacer par le port concerné

# Tuer le processus
kill -9 <PID>
```

**Module non trouvé ?**
```bash
# Installer le module manquant
pip install <nom-du-module>

# Mettre à jour requirements.txt
pip freeze > requirements.txt
```

---

## Ressources

- **FastAPI Docs:** https://fastapi.tiangolo.com
- **Flask Docs:** https://flask.palletsprojects.com
- **OAuth 2.0 RFC:** https://datatracker.ietf.org/doc/html/rfc6749
- **JWT RFC:** https://datatracker.ietf.org/doc/html/rfc7519

---

## Checklist Premier Lancement

- [ ] Python 3.10+ installé (`python3 --version`)
- [ ] Venv créé et activé
- [ ] Dépendances installées (`pip list`)
- [ ] API OAuth2 démarrée (port 8002)
- [ ] Swagger UI accessible (http://127.0.0.1:8002/docs)
- [ ] Authentification testée (Authorize button)
- [ ] Tests automatiques lancés et passés

---

**Temps estimé: 5 minutes** ⏱ 
**Difficulté: Débutant** 🟢

**Besoin d'aide ?** Consultez [README.md](README.md) pour la documentation complète !
