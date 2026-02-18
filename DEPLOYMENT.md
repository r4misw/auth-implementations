# Guide de Déploiement - APIs d'Authentification

Ce guide explique comment déployer les APIs d'authentification sur différentes plateformes.

---

## Table des Matières

1. [Prérequis](#prérequis)
2. [Créer le Repository GitHub](#créer-le-repository-github)
3. [Déploiement sur Heroku](#déploiement-sur-heroku)
4. [Déploiement sur Render](#déploiement-sur-render)
5. [Déploiement sur Railway](#déploiement-sur-railway)
6. [Variables d'Environnement](#variables-denvironnement)
7. [Tests Post-Déploiement](#tests-post-déploiement)

---

## Prérequis

- Git installé (`git --version`)
- Compte GitHub (https://github.com)
- Compte sur une plateforme de déploiement (Heroku, Render, ou Railway)

---

## Créer le Repository GitHub

### 1. Initialiser Git

```bash
cd /home/ubuntu
git init
git add .
git commit -m "Initial commit: Flask & FastAPI authentication APIs (HTTP Basic, JWT, OAuth 2.0)"
```

### 2. Créer le Repository sur GitHub

**Option A: Via l'interface web**
1. Allez sur https://github.com/new
2. Nom du repository: `authentication-apis-learning`
3. Description: `Complete authentication methods: HTTP Basic, JWT, OAuth 2.0 with Flask & FastAPI`
4. **Public** ou **Private** (votre choix)
5. **NE PAS** initialiser avec README (on a déjà le nôtre)
6. Cliquez **Create repository**

**Option B: Via GitHub CLI** (si installé)
```bash
gh repo create authentication-apis-learning --public --source=. --remote=origin --push
```

### 3. Push vers GitHub

Après avoir créé le repo, GitHub vous donne les commandes :

```bash
git remote add origin https://github.com/VOTRE_USERNAME/authentication-apis-learning.git
git branch -M main
git push -u origin main
```

---

## Déploiement sur Heroku

### 1. Installation Heroku CLI

```bash
# Linux/Ubuntu
curl https://cli-assets.heroku.com/install.sh | sh

# macOS (avec Homebrew)
brew tap heroku/brew && brew install heroku

# Vérification
heroku --version
```

### 2. Login et Création App

```bash
# Login Heroku
heroku login

# Créer l'app
heroku create your-auth-api

# Ou laisser Heroku générer un nom
heroku create
```

### 3. Configuration

```bash
# Variables d'environnement
heroku config:set SECRET_KEY="votre-secret-key-super-securisee-ici"
heroku config:set JWT_SECRET_KEY="autre-secret-jwt-different"
heroku config:set ENVIRONMENT="production"

# Ajouter gunicorn au requirements.txt
echo "gunicorn==21.2.0" >> requirements.txt
```

### 4. Choix de l'API à Déployer

Éditez `Procfile` pour choisir quelle API déployer :

**Option 1: Flask HTTP Basic Auth**
```
web: cd projects/flask_http_basic_auth && gunicorn flask_http_basic:app --bind 0.0.0.0:$PORT
```

**Option 2: Flask JWT Auth**
```
web: cd projects/flask_jwt_auth && gunicorn flask_jwt:app --bind 0.0.0.0:$PORT
```

**Option 3: FastAPI OAuth 2.0 (Recommandé)**
```
web: cd fastapi_learning/advanced && uvicorn fastapi_oauth:app --host 0.0.0.0 --port $PORT
```

### 5. Déploiement

```bash
git add .
git commit -m "Add Heroku deployment configuration"
git push heroku main

# Ouvrir l'app
heroku open

# Voir les logs
heroku logs --tail
```

### 6. Accès

- **API:** `https://your-auth-api.herokuapp.com/`
- **Swagger UI (FastAPI):** `https://your-auth-api.herokuapp.com/docs`

---

## Déploiement sur Render

### 1. Créer compte sur Render.com

1. Allez sur https://render.com
2. Créez un compte (gratuit)
3. Connectez votre compte GitHub

### 2. Nouvelle Web Service

1. Dashboard → **New +** → **Web Service**
2. Connectez votre repository GitHub
3. Sélectionnez `authentication-apis-learning`

### 3. Configuration

**Name:** `auth-api` 
**Environment:** `Python 3` 
**Build Command:** `pip install -r requirements.txt` 

**Start Command (choisissez selon l'API):**
- Flask HTTP Basic: `cd projects/flask_http_basic_auth && gunicorn flask_http_basic:app`
- Flask JWT: `cd projects/flask_jwt_auth && gunicorn flask_jwt:app`
- FastAPI OAuth2: `cd fastapi_learning/advanced && uvicorn fastapi_oauth:app --host 0.0.0.0 --port $PORT`

**Plan:** Free

### 4. Variables d'Environnement

Dans l'onglet **Environment** :
```
SECRET_KEY=votre-secret-key-super-securisee
JWT_SECRET_KEY=autre-secret-jwt-different
ENVIRONMENT=production
```

### 5. Déploiement

- Cliquez **Create Web Service**
- Render build et déploie automatiquement
- URL générée: `https://auth-api.onrender.com`

---

## Déploiement sur Railway

### 1. Créer compte Railway

1. Allez sur https://railway.app
2. Connectez avec GitHub
3. Autorisez l'accès

### 2. Nouveau Projet

1. Dashboard → **New Project**
2. **Deploy from GitHub repo**
3. Sélectionnez `authentication-apis-learning`

### 3. Configuration

Railway détecte automatiquement Python. Ajoutez :

**Variables (Settings → Variables):**
```
SECRET_KEY=votre-secret-key-super-securisee
JWT_SECRET_KEY=autre-secret-jwt-different
PORT=8000
```

**Start Command (Settings → Deploy):**
- FastAPI: `cd fastapi_learning/advanced && uvicorn fastapi_oauth:app --host 0.0.0.0 --port $PORT`

### 4. Domaine

- Settings → **Generate Domain**
- URL: `https://your-app.up.railway.app`

---

## Variables d'Environnement

### Génération de Secrets Sécurisés

```bash
# Méthode 1: Python
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Méthode 2: OpenSSL
openssl rand -base64 32

# Méthode 3: UUID
python3 -c "import uuid; print(str(uuid.uuid4()))"
```

### Variables Requises

| Variable | Description | Exemple |
|----------|-------------|---------|
| `SECRET_KEY` | Clé secrète Flask | `k8mP2vN9xQ5tR7wY3zB6cF1dG4hJ8lM0` |
| `JWT_SECRET_KEY` | Clé JWT (différente de SECRET_KEY) | `a9D2fG5hK8mN1qT4wX7zA3cE6iL9oP2s` |
| `ENVIRONMENT` | `production` ou `development` | `production` |
| `PORT` | Port du serveur (auto sur Heroku/Render) | `8000` |

 **IMPORTANT:** Ne JAMAIS commit ces secrets dans Git !

---

## Tests Post-Déploiement

### Test avec cURL

```bash
# Remplacez YOUR_APP_URL par votre URL déployée

# 1. Test route publique
curl https://YOUR_APP_URL/

# 2. OAuth2: Obtenir token
curl -X POST https://YOUR_APP_URL/token \
  -d "username=danieldatascientest" \
  -d "password=datascientest"

# 3. Utiliser le token
TOKEN="votre_token_ici"
curl -H "Authorization: Bearer $TOKEN" \
  https://YOUR_APP_URL/secured
```

### Test avec Swagger UI (FastAPI seulement)

1. Ouvrez `https://YOUR_APP_URL/docs`
2. Cliquez **Authorize** 
3. Entrez credentials
4. Testez les endpoints

---

## Comparaison des Plateformes

| Plateforme | Gratuit | Build Time | Auto-deploy | Domaine Custom |
|------------|---------|------------|-------------|----------------|
| **Heroku** | 550h/mois | ~2-3 min | | (payant) |
| **Render** | 750h/mois | ~1-2 min | | (gratuit) |
| **Railway** | $5 crédit | ~1 min | | (gratuit) |

---

## Troubleshooting

### Erreur: "Application Error"

```bash
# Voir les logs
heroku logs --tail # Heroku
# Ou dans le dashboard Render/Railway
```

### Port Binding Error

Vérifiez que vous utilisez `$PORT` :
```python
# Flask: Ajoutez dans le code
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
```

### Module Not Found

```bash
# Vérifiez requirements.txt
cat requirements.txt

# Rebuild
git add requirements.txt
git commit -m "Update dependencies"
git push
```

---

## Ressources

- **Heroku Python Guide:** https://devcenter.heroku.com/articles/getting-started-with-python
- **Render Docs:** https://render.com/docs
- **Railway Docs:** https://docs.railway.app
- **FastAPI Deployment:** https://fastapi.tiangolo.com/deployment/

---

## Checklist de Déploiement

- [ ] Repository GitHub créé
- [ ] `.gitignore` configuré (ne pas commit venv/, .env)
- [ ] `requirements.txt` à jour
- [ ] Variables d'environnement sécurisées générées
- [ ] Procfile ou Start Command configuré
- [ ] App déployée et accessible
- [ ] Swagger UI fonctionne (FastAPI)
- [ ] Tests avec cURL réussis
- [ ] Documentation mise à jour avec l'URL de production

---

## Félicitations !

Votre API d'authentification est maintenant en ligne et accessible depuis n'importe où !

**Prochaines étapes :**
- Ajouter un domaine personnalisé
- Configurer HTTPS (automatique sur toutes les plateformes)
- Ajouter monitoring (Sentry, New Relic)
- Mettre en place CI/CD avec GitHub Actions
