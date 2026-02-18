"""
Script de tests automatisés pour l'API Flask HTTP Basic Auth
"""

import requests
from requests.auth import HTTPBasicAuth
import base64

# Configuration
BASE_URL = "http://localhost:5000"

# Utilisateurs de test
USERS = {
    "daniel": {
        "password": "datascientest",
        "roles": ["admin", "user"]
    },
    "john": {
        "password": "secret",
        "roles": ["user"]
    }
}


def print_separator():
    print("\n" + "=" * 70)


def test_no_auth():
    """Test : Requête sans authentification (doit renvoyer 401)"""
    print_separator()
    print("TEST 1 : Requête sans authentification")
    print_separator()
    
    response = requests.get(f"{BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Attendu: 401 (Unauthorized)")
    print(f"[OK]" if response.status_code == 401 else "[FAIL]")
    print(f"Response: {response.text[:100]}")


def test_user_access():
    """Test : Accès utilisateur normal (john et daniel)"""
    print_separator()
    print("TEST 2 : Accès route / avec rôle 'user'")
    print_separator()
    
    for username, user_data in USERS.items():
        response = requests.get(
            f"{BASE_URL}/",
            auth=HTTPBasicAuth(username, user_data["password"])
        )
        print(f"\n{username}: Status {response.status_code}")
        print(f"Response: {response.text}")
        print(f"[OK]" if response.status_code == 200 else "[FAIL]")


def test_admin_access():
    """Test : Accès route admin (daniel OK, john KO)"""
    print_separator()
    print("TEST 3 : Accès route /admin avec rôle 'admin'")
    print_separator()
    
    # Daniel (admin) - doit réussir
    response = requests.get(
        f"{BASE_URL}/admin",
        auth=HTTPBasicAuth("daniel", "datascientest")
    )
    print(f"\ndaniel (admin): Status {response.status_code}")
    print(f"Response: {response.text}")
    print(f"[OK]" if response.status_code == 200 else "[FAIL]")
    
    # John (user) - doit échouer avec 403
    response = requests.get(
        f"{BASE_URL}/admin",
        auth=HTTPBasicAuth("john", "secret")
    )
    print(f"\njohn (user): Status {response.status_code}")
    print(f"Response: {response.text[:100]}")
    print(f"[OK] (403 attendu)" if response.status_code == 403 else "[FAIL]")


def test_private_resource():
    """Test : Accès aux ressources privées"""
    print_separator()
    print("TEST 4 : Accès route /private")
    print_separator()
    
    for username, user_data in USERS.items():
        response = requests.get(
            f"{BASE_URL}/private",
            auth=HTTPBasicAuth(username, user_data["password"])
        )
        print(f"\n{username}: Status {response.status_code}")
        print(f"Response: {response.text}")
        print(f"[OK]" if response.status_code == 200 else "[FAIL]")


def test_wrong_password():
    """Test : Mauvais mot de passe (doit renvoyer 401)"""
    print_separator()
    print("TEST 5 : Mauvais mot de passe")
    print_separator()
    
    response = requests.get(
        f"{BASE_URL}/",
        auth=HTTPBasicAuth("daniel", "wrong_password")
    )
    print(f"Status Code: {response.status_code}")
    print(f"Attendu: 401 (Unauthorized)")
    print(f"[OK]" if response.status_code == 401 else "[FAIL]")
    print(f"Response: {response.text[:100]}")


def test_manual_header():
    """Test : Authorization header manuel avec Base64"""
    print_separator()
    print("TEST 6 : Header Authorization manuel (Base64)")
    print_separator()
    
    # Encoder daniel:datascientest en Base64
    credentials = base64.b64encode(b"daniel:datascientest").decode('utf-8')
    print(f"Credentials encodés: {credentials}")
    
    headers = {
        "Authorization": f"Basic {credentials}"
    }
    
    response = requests.get(f"{BASE_URL}/admin", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    print(f"[OK]" if response.status_code == 200 else "[FAIL]")


def demo_base64_encoding():
    """Démonstration de l'encodage Base64"""
    print_separator()
    print("DEMO : Encodage/Décodage Base64")
    print_separator()
    
    examples = [
        ("daniel", "datascientest"),
        ("john", "secret"),
        ("hello", "world")
    ]
    
    for username, password in examples:
        credentials = f"{username}:{password}"
        encoded = base64.b64encode(credentials.encode()).decode()
        decoded = base64.b64decode(encoded).decode()
        
        print(f"\nOriginal:  {credentials}")
        print(f"Encodé:    {encoded}")
        print(f"Décodé:    {decoded}")
        print(f"Header:    Authorization: Basic {encoded}")


if __name__ == "__main__":
    print("\n" + "" * 35)
    print("TESTS API FLASK HTTP BASIC AUTH")
    print("" * 35)
    
    try:
        # Démo encodage
        demo_base64_encoding()
        
        # Tests de l'API
        test_no_auth()
        test_user_access()
        test_admin_access()
        test_private_resource()
        test_wrong_password()
        test_manual_header()
        
        print_separator()
        print(" TOUS LES TESTS TERMINÉS")
        print_separator()
        
    except requests.exceptions.ConnectionError:
        print("\n ERREUR : Impossible de se connecter à l'API")
        print("Assurez-vous que l'API est lancée avec:")
        print("  python flask_http_basic.py")
