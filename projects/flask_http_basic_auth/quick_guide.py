"""
Guide rapide - HTTP Basic Auth avec Flask
"""

# ============================================
# 1. COMPRENDRE L'ENCODAGE BASE64
# ============================================

import base64

# Encoder username:password en Base64
credentials = "daniel:datascientest"
encoded = base64.b64encode(credentials.encode()).decode()
print(f"Original:  {credentials}")
print(f"Encodé:    {encoded}")
print(f"Header:    Authorization: Basic {encoded}")

# Décoder
decoded = base64.b64decode(encoded).decode()
print(f"Décodé:    {decoded}\n")


# ============================================
# 2. TESTER L'API AVEC REQUESTS
# ============================================

import requests
from requests.auth import HTTPBasicAuth

BASE_URL = "http://localhost:5000"

print("=" * 70)
print("TESTS DE L'API FLASK HTTP BASIC AUTH")
print("=" * 70)

# Test 1: Sans authentification (401)
print("\n1. Test sans authentification:")
try:
    response = requests.get(f"{BASE_URL}/")
    print(f"   Status: {response.status_code}  (Attendu: 401)")
except Exception as e:
    print(f"   Erreur: {e}")

# Test 2: Avec daniel (admin + user)
print("\n2. Test avec daniel (admin):")
response = requests.get(
    f"{BASE_URL}/admin",
    auth=HTTPBasicAuth('daniel', 'datascientest')
)
print(f"   Status: {response.status_code} ")
print(f"   Response: {response.text}")

# Test 3: Avec john sur route admin (403)
print("\n3. Test avec john sur /admin (devrait échouer):")
response = requests.get(
    f"{BASE_URL}/admin",
    auth=HTTPBasicAuth('john', 'secret')
)
print(f"   Status: {response.status_code}  (Attendu: 403)")

# Test 4: Ressources privées
print("\n4. Test ressources privées:")
for user, password in [('daniel', 'datascientest'), ('john', 'secret')]:
    response = requests.get(
        f"{BASE_URL}/private",
        auth=(user, password)  # Syntaxe courte
    )
    print(f"   {user}: {response.text}")


# ============================================
# 3. HEADER AUTHORIZATION MANUEL
# ============================================

print("\n" + "=" * 70)
print("HEADER AUTHORIZATION MANUEL")
print("=" * 70)

credentials_base64 = base64.b64encode(b"daniel:datascientest").decode()
headers = {
    "Authorization": f"Basic {credentials_base64}"
}

response = requests.get(f"{BASE_URL}/", headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")


# ============================================
# 4. COMPRENDRE LE SYSTÈME DE RÔLES
# ============================================

print("\n" + "=" * 70)
print("SYSTÈME DE RÔLES")
print("=" * 70)

users = {
    "daniel": {
        "roles": ["admin", "user"],
        "accès": "/, /admin, /private"
    },
    "john": {
        "roles": ["user"],
        "accès": "/, /private"
    }
}

for username, info in users.items():
    print(f"\n{username.upper()}:")
    print(f"  Rôles: {', '.join(info['roles'])}")
    print(f"  Peut accéder: {info['accès']}")


# ============================================
# 5. CODES HTTP IMPORTANTS
# ============================================

print("\n" + "=" * 70)
print("CODES HTTP")
print("=" * 70)

codes = {
    200: " OK - Authentification et autorisation réussies",
    401: " Unauthorized - Pas d'authentification ou mauvais credentials",
    403: " Forbidden - Authentifié mais pas les droits pour cette ressource"
}

for code, description in codes.items():
    print(f"{code}: {description}")


print("\n" + "=" * 70)
print(" SÉCURITÉ: Utilisez toujours HTTPS en production !")
print("   Base64 n'est PAS du chiffrement, juste de l'encodage")
print("=" * 70)
