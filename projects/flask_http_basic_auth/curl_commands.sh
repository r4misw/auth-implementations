# Commandes curl pour tester l'API Flask HTTP Basic Auth

# ============================================
# 1. TEST SANS AUTHENTIFICATION (401)
# ============================================
curl http://localhost:5000/

# ============================================
# 2. TESTS AVEC DANIEL (admin + user)
# ============================================

# Route / (user)
curl -u daniel:datascientest http://localhost:5000/

# Route /admin (admin)
curl -u daniel:datascientest http://localhost:5000/admin

# Route /private (user)
curl -u daniel:datascientest http://localhost:5000/private


# ============================================
# 3. TESTS AVEC JOHN (user seulement)
# ============================================

# Route / (user) - OK
curl -u john:secret http://localhost:5000/

# Route /private (user) - OK
curl -u john:secret http://localhost:5000/private

# Route /admin (admin) - ERREUR 403 Forbidden
curl -u john:secret http://localhost:5000/admin


# ============================================
# 4. HEADER AUTHORIZATION MANUEL (Base64)
# ============================================

# daniel:datascientest encodé en Base64 = ZGFuaWVsOmRhdGFzY2llbnRlc3Q=
curl -H "Authorization: Basic ZGFuaWVsOmRhdGFzY2llbnRlc3Q=" http://localhost:5000/admin

# john:secret encodé en Base64 = am9objpzZWNyZXQ=
curl -H "Authorization: Basic am9objpzZWNyZXQ=" http://localhost:5000/


# ============================================
# 5. TESTS AVEC MAUVAIS MOT DE PASSE (401)
# ============================================
curl -u daniel:wrong_password http://localhost:5000/


# ============================================
# 6. VOIR LES HEADERS DE RÉPONSE
# ============================================
curl -i http://localhost:5000/
# Note: Le header WWW-Authenticate: Basic realm="Authentication Required" sera visible


# ============================================
# 7. VERSION VERBOSE POUR DEBUGGING
# ============================================
curl -v -u daniel:datascientest http://localhost:5000/admin


# ============================================
# ENCODAGE BASE64 EN LIGNE DE COMMANDE
# ============================================

# Encoder des credentials
echo -n "daniel:datascientest" | base64
# Résultat: ZGFuaWVsOmRhdGFzY2llbnRlc3Q=

echo -n "john:secret" | base64
# Résultat: am9objpzZWNyZXQ=

# Décoder
echo "ZGFuaWVsOmRhdGFzY2llbnRlc3Q=" | base64 -d
# Résultat: daniel:datascientest
