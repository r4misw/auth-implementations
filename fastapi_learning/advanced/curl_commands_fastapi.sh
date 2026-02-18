# Commandes curl pour tester FastAPI HTTP Basic Auth

# ============================================
# 1. ROUTE PUBLIQUE (pas d'authentification)
# ============================================
curl http://localhost:8000/


# ============================================
# 2. TEST SANS AUTHENTIFICATION (401)
# ============================================
curl -X GET -i http://localhost:8000/user
# Résultat: 401 Unauthorized avec header WWW-Authenticate: Basic


# ============================================
# 3. TESTS AVEC DANIEL
# ============================================

# Route /user
curl -u daniel:datascientest http://localhost:8000/user
# Résultat: "Hello daniel"

# Route /me
curl -u daniel:datascientest http://localhost:8000/me
# Résultat: {"username":"daniel","name":"Daniel Datascientest"}


# ============================================
# 4. TESTS AVEC JOHN
# ============================================

# Route /user
curl -u john:secret http://localhost:8000/user
# Résultat: "Hello john"

# Route /me
curl -u john:secret http://localhost:8000/me
# Résultat: {"username":"john","name":"John Datascientest"}


# ============================================
# 5. HEADER AUTHORIZATION MANUEL (Base64)
# ============================================

# daniel:datascientest encodé en Base64 = ZGFuaWVsOmRhdGFzY2llbnRlc3Q=
curl -X GET http://localhost:8000/user \
  -H 'Authorization: Basic ZGFuaWVsOmRhdGFzY2llbnRlc3Q='

# john:secret encodé en Base64 = am9objpzZWNyZXQ=
curl -X GET http://localhost:8000/user \
  -H 'Authorization: Basic am9objpzZWNyZXQ='


# ============================================
# 6. TESTS AVEC MAUVAIS CREDENTIALS (401)
# ============================================

# Mauvais mot de passe
curl -i -u daniel:wrongpassword http://localhost:8000/user
# Résultat: 401 Unauthorized

# Username inexistant
curl -i -u hacker:trytobreak http://localhost:8000/user
# Résultat: 401 Unauthorized


# ============================================
# 7. VOIR LES HEADERS COMPLETS
# ============================================
curl -v -u daniel:datascientest http://localhost:8000/user
# L'option -v affiche tous les headers envoyés et reçus


# ============================================
# 8. DOCUMENTATION INTERACTIVE
# ============================================

# Swagger UI (interface interactive)
curl http://localhost:8000/docs
# Ouvrir dans un navigateur: http://localhost:8000/docs

# ReDoc (documentation alternative)
curl http://localhost:8000/redoc
# Ouvrir dans un navigateur: http://localhost:8000/redoc

# OpenAPI JSON schema
curl http://localhost:8000/openapi.json


# ============================================
# 9. ENCODAGE/DÉCODAGE BASE64
# ============================================

# Encoder des credentials
echo -n "daniel:datascientest" | base64
# Résultat: ZGFuaWVsOmRhdGFzY2llbnRlc3Q=

echo -n "john:secret" | base64
# Résultat: am9objpzZWNyZXQ=

# Décoder (ATTENTION: c'est FACILE !)
echo "ZGFuaWVsOmRhdGFzY2llbnRlc3Q=" | base64 -d
# Résultat: daniel:datascientest

echo "am9objpzZWNyZXQ=" | base64 -d
# Résultat: john:secret


# ============================================
# 10. TESTS AVEC JQ (formater JSON)
# ============================================

# Si jq est installé, formater les réponses JSON
curl http://localhost:8000/ | jq
curl -u daniel:datascientest http://localhost:8000/me | jq


# ============================================
# 11. COMPARAISON AVEC FLASK (port 5000)
# ============================================

# Flask (port 5000)
curl -u daniel:datascientest http://localhost:5000/

# FastAPI (port 8000)
curl -u daniel:datascientest http://localhost:8000/user

# Les deux utilisent le même format d'authentification !
