# Commandes curl pour tester Flask JWT Authentication

# ============================================
# 1. ROUTE PUBLIQUE
# ============================================
curl http://127.0.0.1:5001/


# ============================================
# 2. AUTHENTIFICATION - OBTENIR UN TOKEN
# ============================================

# Avec danieldatascientest
curl -X POST -H "Content-Type: application/json" \
  -d '{"username":"danieldatascientest", "password":"datascientest"}' \
  http://127.0.0.1:5001/login

# Avec johndatascientest
curl -X POST -H "Content-Type: application/json" \
  -d '{"username":"johndatascientest", "password":"secret"}' \
  http://127.0.0.1:5001/login

# Sauvegarder le token dans une variable
TOKEN=$(curl -s -X POST -H "Content-Type: application/json" \
  -d '{"username":"danieldatascientest", "password":"datascientest"}' \
  http://127.0.0.1:5001/login | jq -r '.access_token')

echo "Token obtenu: $TOKEN"


# ============================================
# 3. UTILISER LE TOKEN - ROUTES PROTÉGÉES
# ============================================

# Route /user (affiche l'utilisateur connecté)
curl -X GET -H "Authorization: Bearer $TOKEN" \
  http://127.0.0.1:5001/user

# Route /resource (affiche la ressource de l'utilisateur)
curl -X GET -H "Authorization: Bearer $TOKEN" \
  http://127.0.0.1:5001/resource


# ============================================
# 4. TESTS D'ERREURS
# ============================================

# Sans token (erreur 401)
curl -i -X GET http://127.0.0.1:5001/user

# Mauvais credentials (erreur 401)
curl -X POST -H "Content-Type: application/json" \
  -d '{"username":"hacker", "password":"wrongpass"}' \
  http://127.0.0.1:5001/login

# Token invalide (erreur 422 ou 401)
curl -i -X GET -H "Authorization: Bearer INVALID_TOKEN" \
  http://127.0.0.1:5001/user


# ============================================
# 5. WORKFLOW COMPLET AUTOMATISÉ
# ============================================

#!/bin/bash
echo "=== WORKFLOW JWT COMPLET ==="

# 1. Login
echo -e "\n1. Login..."
TOKEN=$(curl -s -X POST -H "Content-Type: application/json" \
  -d '{"username":"danieldatascientest", "password":"datascientest"}' \
  http://127.0.0.1:5001/login | jq -r '.access_token')

if [ -z "$TOKEN" ] || [ "$TOKEN" = "null" ]; then
    echo " Échec de l'authentification"
    exit 1
fi

echo " Token obtenu: ${TOKEN:0:50}..."

# 2. Accéder à /user
echo -e "\n2. Accès à /user..."
RESPONSE=$(curl -s -X GET -H "Authorization: Bearer $TOKEN" \
  http://127.0.0.1:5001/user)
echo " $RESPONSE"

# 3. Accéder à /resource
echo -e "\n3. Accès à /resource..."
RESPONSE=$(curl -s -X GET -H "Authorization: Bearer $TOKEN" \
  http://127.0.0.1:5001/resource)
echo " $RESPONSE"

echo -e "\n=== WORKFLOW TERMINÉ ==="


# ============================================
# 6. DÉCODER UN JWT (afficher le contenu)
# ============================================

# Méthode 1: Avec jq et base64
echo $TOKEN | cut -d'.' -f2 | base64 -d 2>/dev/null | jq

# Méthode 2: Avec Python
python3 << 'EOF'
import jwt
import sys
import json

token = "$TOKEN"  # Remplacer par votre token
try:
    decoded = jwt.decode(token, options={"verify_signature": False})
    print(json.dumps(decoded, indent=2))
except Exception as e:
    print(f"Erreur: {e}")
EOF


# ============================================
# 7. VÉRIFIER L'EXPIRATION
# ============================================

python3 << 'EOF'
import jwt
from datetime import datetime

token = "$TOKEN"  # Remplacer par votre token
decoded = jwt.decode(token, options={"verify_signature": False})

exp = decoded.get('exp')
if exp:
    exp_time = datetime.fromtimestamp(exp)
    now = datetime.now()
    remaining = (exp_time - now).total_seconds() / 60
    
    print(f"Token expire à: {exp_time}")
    print(f"Temps restant: {remaining:.1f} minutes")
    
    if remaining <= 0:
        print("  Token EXPIRÉ !")
    elif remaining < 5:
        print("  Token expire bientôt !")
    else:
        print(" Token valide")
EOF


# ============================================
# 8. TESTER AVEC PLUSIEURS UTILISATEURS
# ============================================

echo "=== TESTS MULTI-UTILISATEURS ==="

# Daniel
TOKEN_DANIEL=$(curl -s -X POST -H "Content-Type: application/json" \
  -d '{"username":"danieldatascientest", "password":"datascientest"}' \
  http://127.0.0.1:5001/login | jq -r '.access_token')

echo "Daniel:"
curl -s -X GET -H "Authorization: Bearer $TOKEN_DANIEL" \
  http://127.0.0.1:5001/resource | jq

# John
TOKEN_JOHN=$(curl -s -X POST -H "Content-Type: application/json" \
  -d '{"username":"johndatascientest", "password":"secret"}' \
  http://127.0.0.1:5001/login | jq -r '.access_token')

echo "John:"
curl -s -X GET -H "Authorization: Bearer $TOKEN_JOHN" \
  http://127.0.0.1:5001/resource | jq


# ============================================
# 9. VERSION AVEC OUTPUT FORMATÉ
# ============================================

echo ""
echo "   FLASK JWT AUTHENTICATION TEST        "
echo ""

echo -e "\n Login..."
RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" \
  -d '{"username":"danieldatascientest", "password":"datascientest"}' \
  http://127.0.0.1:5001/login)

TOKEN=$(echo $RESPONSE | jq -r '.access_token')

if [ "$TOKEN" != "null" ]; then
    echo " Authentication réussie"
    echo " Token: ${TOKEN:0:40}..."
    
    echo -e "\n Récupération utilisateur..."
    curl -s -X GET -H "Authorization: Bearer $TOKEN" \
      http://127.0.0.1:5001/user | jq
    
    echo -e "\n Récupération ressource..."
    curl -s -X GET -H "Authorization: Bearer $TOKEN" \
      http://127.0.0.1:5001/resource | jq
else
    echo " Authentication échouée"
fi


# ============================================
# 10. BENCHMARK - TEMPS DE RÉPONSE
# ============================================

echo "=== BENCHMARK ===" 

# Login
echo "Login:"
time curl -s -X POST -H "Content-Type: application/json" \
  -d '{"username":"danieldatascientest", "password":"datascientest"}' \
  http://127.0.0.1:5001/login > /dev/null

# Route protégée
echo -e "\nRoute protégée:"
time curl -s -X GET -H "Authorization: Bearer $TOKEN" \
  http://127.0.0.1:5001/user > /dev/null
