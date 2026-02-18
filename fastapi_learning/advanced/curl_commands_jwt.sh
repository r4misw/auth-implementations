#!/bin/bash

# Commandes curl pour tester FastAPI JWT Authentication

# ============================================
# 1. ROUTE PUBLIQUE
# ============================================
echo "=== 1. Route publique ==="
curl http://127.0.0.1:8001/
echo -e "\n"


# ============================================
# 2. INSCRIPTION (SIGNUP)
# ============================================
echo "=== 2. Inscription (signup) ==="

# Inscription daniel
curl -X POST -i \
  http://127.0.0.1:8001/user/signup \
  -d '{"username": "daniel", "password": "datascientest"}' \
  -H 'Content-Type: application/json'

echo -e "\n"

# Inscription john
curl -X POST -i \
  http://127.0.0.1:8001/user/signup \
  -d '{"username": "john", "password": "secret"}' \
  -H 'Content-Type: application/json'

echo -e "\n"


# ============================================
# 3. CONNEXION (LOGIN)
# ============================================
echo "=== 3. Connexion (login) ==="

# Login daniel
curl -X POST -i \
  http://127.0.0.1:8001/user/login \
  -d '{"username": "daniel", "password": "datascientest"}' \
  -H 'Content-Type: application/json'

echo -e "\n"


# ============================================
# 4. SAUVEGARDER LE TOKEN
# ============================================
echo "=== 4. Récupération et sauvegarde du token ==="

TOKEN=$(curl -s -X POST \
  http://127.0.0.1:8001/user/signup \
  -d '{"username": "testuser", "password": "testpass"}' \
  -H 'Content-Type: application/json' | jq -r '.access_token')

echo "Token obtenu: $TOKEN"
echo -e "\n"


# ============================================
# 5. UTILISER LE TOKEN
# ============================================
echo "=== 5. Route sécurisée avec token ==="

curl -X GET -i http://127.0.0.1:8001/secured \
  -H "Authorization: Bearer $TOKEN"

echo -e "\n"


# ============================================
# 6. TESTS D'ERREURS
# ============================================
echo "=== 6. Tests d'erreurs ==="

# Sans token (erreur 403)
echo "6a. Sans token (403 attendu):"
curl -i -X GET http://127.0.0.1:8001/secured
echo -e "\n"

# Token invalide (erreur 403)
echo "6b. Token invalide (403 attendu):"
curl -i -X GET http://127.0.0.1:8001/secured \
  -H "Authorization: Bearer INVALID_TOKEN"
echo -e "\n"

# Mauvais credentials
echo "6c. Mauvais credentials:"
curl -X POST -i \
  http://127.0.0.1:8001/user/login \
  -d '{"username": "hacker", "password": "wrongpass"}' \
  -H 'Content-Type: application/json'
echo -e "\n"


# ============================================
# 7. WORKFLOW COMPLET
# ============================================
echo "=== 7. Workflow complet automatisé ==="

# 1. Signup
echo "Étape 1/3: Inscription..."
TOKEN=$(curl -s -X POST \
  http://127.0.0.1:8001/user/signup \
  -d '{"username": "alice", "password": "wonderland"}' \
  -H 'Content-Type: application/json' | jq -r '.access_token')

if [ -z "$TOKEN" ] || [ "$TOKEN" = "null" ]; then
    echo " Échec de l'inscription"
    exit 1
fi

echo " Token obtenu: ${TOKEN:0:50}..."

# 2. Accéder à la route sécurisée
echo -e "\nÉtape 2/3: Accès route sécurisée..."
RESPONSE=$(curl -s -X GET http://127.0.0.1:8001/secured \
  -H "Authorization: Bearer $TOKEN")

if echo "$RESPONSE" | grep -q "secured"; then
    echo " Accès autorisé: $RESPONSE"
else
    echo " Accès refusé: $RESPONSE"
fi

# 3. Login avec les mêmes credentials
echo -e "\nÉtape 3/3: Login avec mêmes credentials..."
LOGIN_TOKEN=$(curl -s -X POST \
  http://127.0.0.1:8001/user/login \
  -d '{"username": "alice", "password": "wonderland"}' \
  -H 'Content-Type: application/json' | jq -r '.access_token')

if [ -z "$LOGIN_TOKEN" ] || [ "$LOGIN_TOKEN" = "null" ]; then
    echo " Échec du login"
else
    echo " Login réussi: ${LOGIN_TOKEN:0:50}..."
fi

echo -e "\n Workflow terminé!\n"


# ============================================
# 8. DÉCODER UN JWT
# ============================================
echo "=== 8. Décoder un JWT (afficher le contenu) ==="

# Méthode 1: Avec jq et base64
echo "Payload décodé:"
echo $TOKEN | cut -d'.' -f2 | base64 -d 2>/dev/null | jq
echo -e "\n"


# ============================================
# 9. VERSION PYTHON
# ============================================
echo "=== 9. Exemple avec Python ==="

python3 << 'EOF'
import requests
import json

# Signup
response = requests.post(
    url="http://127.0.0.1:8001/user/signup",
    json={
        "username": "pythonuser",
        "password": "pythonpass"
    }
)

if response.status_code == 200:
    token = response.json()["access_token"]
    print(f" Token reçu: {token[:50]}...\n")
    
    # Utiliser le token
    response_secured = requests.get(
        url="http://127.0.0.1:8001/secured",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    
    if response_secured.status_code == 200:
        print(f" Route sécurisée: {response_secured.json()}")
    else:
        print(f" Erreur: {response_secured.status_code}")
else:
    print(f" Échec signup: {response.status_code}")
EOF

echo -e "\n"


# ============================================
# 10. VÉRIFIER L'EXPIRATION
# ============================================
echo "=== 10. Vérifier l'expiration du token ==="

python3 << EOF
import jwt
from datetime import datetime

token = "$TOKEN"
decoded = jwt.decode(token, options={"verify_signature": False})

exp = decoded.get('expires')
if exp:
    exp_time = datetime.fromtimestamp(exp)
    now = datetime.now()
    remaining = (exp_time - now).total_seconds() / 60
    
    print(f"Token expire à: {exp_time}")
    print(f"Temps restant: {remaining:.1f} minutes")
    
    if remaining <= 0:
        print("  Token EXPIRÉ !")
    elif remaining < 2:
        print("  Token expire bientôt !")
    else:
        print(" Token valide")
EOF

echo -e "\n"


# ============================================
# 11. COMPARAISON AVEC FLASK JWT
# ============================================
echo "=== 11. Comparaison FastAPI vs Flask JWT ==="

echo "FastAPI JWT (port 8001):"
curl -s http://127.0.0.1:8001/ | jq '.message'

echo -e "\nFlask JWT (port 5001):"
curl -s http://127.0.0.1:5001/ | jq '.message' 2>/dev/null || echo "  Flask JWT non démarré"

echo -e "\n"


# ============================================
# 12. BENCHMARK
# ============================================
echo "=== 12. Benchmark - Temps de réponse ==="

echo "Signup:"
time curl -s -X POST \
  http://127.0.0.1:8001/user/signup \
  -d '{"username": "benchmark", "password": "test"}' \
  -H 'Content-Type: application/json' > /dev/null

echo -e "\nRoute sécurisée:"
time curl -s -X GET http://127.0.0.1:8001/secured \
  -H "Authorization: Bearer $TOKEN" > /dev/null

echo -e "\n"


# ============================================
# 13. DOCUMENTATION SWAGGER
# ============================================
echo "=== 13. Documentation Swagger ==="
echo " Swagger UI:  http://127.0.0.1:8001/docs"
echo " ReDoc:       http://127.0.0.1:8001/redoc"
echo ""
echo " Conseil: Teste l'API directement dans Swagger UI!"
