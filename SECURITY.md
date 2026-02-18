# Guide de Sécurité - HTTPS et Cryptage

Ce guide explique comment fonctionnent HTTPS et pourquoi il est essentiel de protéger votre API.

---

## Table des matières

1. [L'attaque Man in the Middle](#lattaque-man-in-the-middle)
2. [Cryptage Symétrique](#cryptage-symétrique)
3. [Cryptage Asymétrique](#cryptage-asymétrique)
4. [HTTPS en Production](#https-en-production)
5. [Démonstration Pratique](#démonstration-pratique)

---

## L'attaque Man in the Middle

L'objectif principal de HTTPS est de protéger les communications entre un client et un serveur. Sans HTTPS, les données peuvent être interceptées entre le client et le serveur. Un "man in the middle" (personne au milieu) peut :

- Lire les données non chiffrées
- Modifier les messages
- Se faire passer pour le serveur ou le client

HTTPS résout ce problème avec deux mécanismes :

1. **Chiffrement** : Rendre les données illisibles
2. **Authentification** : Vérifier l'identité du serveur

---

## Cryptage Symétrique

Le cryptage symétrique est simple : deux utilisateurs partagent la même clé pour chiffrer ET déchiffrer les messages.

### Analogie

Imaginez Alice et Bob qui s'échangent des messages dans une boîte fermée avec un cadenas :

```
Alice --> [Message chiffré avec clé K] --> Bob
          [Bob ouvre avec clé K]
```

### Le Problème

Alice doit envoyer la clé à Bob d'une manière sécurisée. Si quelqu'un intercepte la clé, il peut décrypter tous les messages.

```
Attaquant intercepte : [Message] + [Clé]  --> Peut tout lire!
```

### Conclusion

Le chiffrement symétrique est rapide mais nécessite un échange sécurisé de la clé, ce qui est difficile à réaliser sur Internet.

---

## Cryptage Asymétrique

Le cryptage asymétrique résout le problème de partage de clé en utilisant deux clés différentes : une **publique** et une **privée**.

### Clés Privées et Publiques

Chaque utilisateur a une paire de clés :

- **Clé Privée** : Secrète, jamais partagée
- **Clé Publique** : Peut être communiquée à n'importe qui

```
Alice                          Bob
|                              |
Private Key A (secret)         Private Key B (secret)
Public Key A (communiquée)     Public Key B (communiquée)
```

### Chiffrement Asymétrique

Pour envoyer un message à Bob :

1. Alice chiffre avec la **clé publique de Bob**
2. Bob déchiffre avec sa **clé privée**

```
Alice envoie : Encrypt(message, PublicKey_Bob)
                        |
                        v
Bob reçoit : Decrypt(encrypted_message, PrivateKey_Bob) = message
```

Seul Bob peut lire le message car seul Bob possède sa clé privée.

### Signature Numérique

Pour prouver l'identité de l'expéditeur, Alice peut **signer** le message :

1. Créer un hash du message
2. Signer le hash avec sa **clé privée**
3. Envoyer le message + la signature

```
Alice signe :
message --> hash --> Sign(hash, PrivateKey_Alice) = signature

Bob vérifie :
signature --> Verify(signature, PublicKey_Alice) = hash original
```

Bob peut maintenant vérifier que Alice a envoyé le message car seule la clé privée d'Alice peut créer cette signature.

---

## HTTPS en Production

### Comment Fonctionne HTTPS

HTTPS combine asymétrique et symétrique :

1. **Handshake (Asymétrique)** : Établir une connexion sécurisée
   - Client et serveur échangent des certificats
   - Ils négocient une clé symétrique temporaire

2. **Communication (Symétrique)** : Chiffrer les données
   - Les données sont chiffrées avec la clé symétrique (rapide)
   - Utilisée uniquement pour cette session

### Certificats SSL/TLS

Un certificat X.509 contient :
- La clé publique du serveur
- L'identité du serveur (domaine)
- La signature de l'autorité de certification (CA)

```
Certificate:
  Subject: CN = example.com
  Public Key: -----BEGIN RSA PUBLIC KEY-----
  Issuer: Let's Encrypt (trusted CA)
  Signature: [Signé par Let's Encrypt]
```

### Autorités de Certification (CA)

Les CA sont des organismes de confiance qui :
- Vérifient l'identité du propriétaire du domaine
- Signent le certificat avec leur clé privée
- Vous pouvez vérifier la signature car vous avez leur clé publique

### Configuration HTTPS pour FastAPI/Flask

#### FastAPI avec Uvicorn

```bash
# Générer un certificat auto-signé (développement uniquement)
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# Lancer avec HTTPS
uvicorn fastapi_oauth:app --ssl-keyfile=key.pem --ssl-certfile=cert.pem --host 0.0.0.0 --port 443
```

#### Flask avec Gunicorn

```bash
gunicorn --certfile=cert.pem --keyfile=key.pem --bind 0.0.0.0:443 app:app
```

#### En Production (Heroku, Render, Railway)

Ces plateformes fournissent HTTPS automatiquement avec Let's Encrypt.

**Aucune configuration supplémentaire nécessaire !**

---

## Démonstration Pratique

### Génération de Clés

```bash
# Générer une clé privée RSA 2048 bits
openssl genrsa -out my_private.key 2048

# Extraire la clé publique
openssl rsa -in my_private.key -pubout -out my_public.key
```

### Chiffrement et Déchiffrement

```bash
# Créer un message
echo "Hi Bob" > my_message.txt

# Chiffrer avec la clé publique de Bob
openssl rsautl -encrypt -pubin -inkey bob_public.key -in my_message.txt -out encrypted_message

# Déchiffrer avec la clé privée de Bob
openssl rsautl -decrypt -inkey bob_private.key -in encrypted_message
```

### Signature Numérique

```bash
# Créer un hash du message
md5sum my_message.txt > my_hash.txt

# Signer le hash avec la clé privée d'Alice
openssl rsautl -sign -inkey alice_private.key -in my_hash.txt -out alice_signature.txt

# Bob vérifie la signature avec la clé publique d'Alice
openssl rsautl -verify -pubin -inkey alice_public.key -in alice_signature.txt

# Vérifier que le hash correspond
openssl rsautl -verify -pubin -inkey alice_public.key -in alice_signature.txt > hash_from_signature.txt
md5sum my_message.txt > hash_from_message.txt
diff hash_from_signature.txt hash_from_message.txt  # Doit être identique
```

---

## Bonnes Pratiques de Sécurité pour Votre API

### 1. Toujours Utiliser HTTPS

```python
# Correct - Force HTTPS
@app.get("/secured")
async def secured_route(current_user: User = Depends(get_current_user)):
    return current_user

# Meilleur - Avec redirection HTTP vers HTTPS
# Configuration à faire au niveau du reverse proxy (Nginx, Apache)
```

### 2. Secrets Sécurisés

**Ne jamais commiter :**
```
.env files
secret_key.txt
private_keys/
passwords.txt
```

**Ils doivent être dans des variables d'environnement :**
```python
import os
SECRET_KEY = os.getenv("SECRET_KEY")
JWT_SECRET = os.getenv("JWT_SECRET_KEY")
```

### 3. Tokens JWT avec HTTPS

```python
from datetime import datetime, timedelta
from jose import jwt

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    
    # IMPORTANT: Utiliser une clé secrète forte
    encoded_jwt = jwt.encode(
        to_encode,
        os.getenv("JWT_SECRET_KEY"),
        algorithm="HS256"
    )
    return encoded_jwt
```

### 4. Authentification Basique Seulement sur HTTPS

```python
from fastapi import HTTPException, status
from fastapi.security import HTTPBasic, HTTPAuthorizationCredentials

security = HTTPBasic()

@app.get("/")
async def root(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # HTTPS sécurise la transmission du mot de passe en base64
    # HTTP exposerait le mot de passe en clair
    return {"user": credentials.username}
```

### 5. Headers de Sécurité Essentiels

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI()

# Middleware pour CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],  # Spécifier exactement
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Headers de sécurité
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response
```

---

## Résumé des Points Clés

| Concept | Clé | Détails |
|---------|-----|---------|
| **Symétrique** | Une clé partagée | Rapide mais difficile à partager |
| **Asymétrique** | Paire (privée + publique) | Sûr, utilisé pour l'authentification |
| **HTTPS** | Asymétrique + Symétrique | Sécurise tout Internet |
| **Certificat** | X.509 signé par CA | Prouve l'identité du serveur |
| **JWT** | Signature asymétrique | Token d'authentification stateless |
| **Production** | HTTPS obligatoire | Heroku, Render, Railway = automatique |

---

## Ressources

- **OpenSSL Manual** : https://www.openssl.org/docs/
- **RFC 5246 TLS 1.2** : https://tools.ietf.org/html/rfc5246
- **OWASP API Security** : https://owasp.org/www-project-api-security/
- **Let's Encrypt** : https://letsencrypt.org/
- **FastAPI Security** : https://fastapi.tiangolo.com/advanced/security/

---

En production, vous n'avez pas à vous soucier de HTTPS. Les plateformes comme Heroku, Render et Railway le gèrent automatiquement avec Let's Encrypt !
