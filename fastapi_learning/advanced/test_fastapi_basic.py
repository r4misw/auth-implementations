"""
Tests automatisés pour FastAPI HTTP Basic Auth
"""

import requests
from requests.auth import HTTPBasicAuth
import base64
import json

# Configuration
BASE_URL = "http://localhost:8000"

# Couleurs pour l'affichage
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def print_separator():
    print("\n" + "=" * 70)


def print_test(title):
    print_separator()
    print(f"{BLUE}{title}{RESET}")
    print_separator()


def print_success(message):
    print(f"{GREEN}[OK]{RESET}: {message}")


def print_error(message):
    print(f"{RED}[FAIL]{RESET}: {message}")


def print_info(message):
    print(f"{YELLOW}ℹ  INFO{RESET}: {message}")


def test_public_route():
    """Test: Route publique / (accessible sans authentification)"""
    print_test("TEST 1: Route publique /")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        
        if response.status_code == 200:
            print_success(f"Status {response.status_code}")
            data = response.json()
            print(f"Message: {data['message']}")
            print(f"Users disponibles: {', '.join(data['users'])}")
            print(f"Endpoints: {json.dumps(data['endpoints'], indent=2)}")
        else:
            print_error(f"Status {response.status_code} (Attendu: 200)")
            
    except Exception as e:
        print_error(f"Erreur: {e}")


def test_no_auth():
    """Test: Requête sans authentification sur route protégée (401)"""
    print_test("TEST 2: Requête sans authentification sur /user")
    
    try:
        response = requests.get(f"{BASE_URL}/user")
        
        if response.status_code == 401:
            print_success(f"Status {response.status_code} (Unauthorized)")
            
            # Vérifier le header WWW-Authenticate
            if 'www-authenticate' in response.headers:
                print_info(f"Header: {response.headers['www-authenticate']}")
            
        else:
            print_error(f"Status {response.status_code} (Attendu: 401)")
            
    except Exception as e:
        print_error(f"Erreur: {e}")


def test_daniel_auth():
    """Test: Authentification avec daniel"""
    print_test("TEST 3: Authentification avec daniel")
    
    tests = [
        ("/user", "Message de bienvenue"),
        ("/me", "Informations utilisateur"),
    ]
    
    for endpoint, description in tests:
        try:
            response = requests.get(
                f"{BASE_URL}{endpoint}",
                auth=HTTPBasicAuth('daniel', 'datascientest')
            )
            
            if response.status_code == 200:
                print_success(f"{endpoint}: {response.text[:100]}")
            else:
                print_error(f"{endpoint}: Status {response.status_code}")
                
        except Exception as e:
            print_error(f"{endpoint}: {e}")


def test_john_auth():
    """Test: Authentification avec john"""
    print_test("TEST 4: Authentification avec john")
    
    try:
        response = requests.get(
            f"{BASE_URL}/user",
            auth=('john', 'secret')  # Syntaxe courte
        )
        
        if response.status_code == 200:
            print_success(f"Status {response.status_code}")
            print(f"Response: {response.text}")
        else:
            print_error(f"Status {response.status_code}")
            
    except Exception as e:
        print_error(f"Erreur: {e}")


def test_wrong_password():
    """Test: Mauvais mot de passe (401)"""
    print_test("TEST 5: Mauvais mot de passe")
    
    try:
        response = requests.get(
            f"{BASE_URL}/user",
            auth=HTTPBasicAuth('daniel', 'wrongpassword')
        )
        
        if response.status_code == 401:
            print_success(f"Status {response.status_code} (Rejeté comme attendu)")
            print_info(f"Message: {response.json()['detail']}")
        else:
            print_error(f"Status {response.status_code} (Attendu: 401)")
            
    except Exception as e:
        print_error(f"Erreur: {e}")


def test_wrong_username():
    """Test: Username inexistant (401)"""
    print_test("TEST 6: Username inexistant")
    
    try:
        response = requests.get(
            f"{BASE_URL}/user",
            auth=HTTPBasicAuth('hacker', 'trytobreak')
        )
        
        if response.status_code == 401:
            print_success(f"Status {response.status_code} (Rejeté comme attendu)")
        else:
            print_error(f"Status {response.status_code} (Attendu: 401)")
            
    except Exception as e:
        print_error(f"Erreur: {e}")


def test_manual_base64_header():
    """Test: Header Authorization manuel avec Base64"""
    print_test("TEST 7: Header Authorization manuel (Base64)")
    
    # Encoder daniel:datascientest
    credentials = base64.b64encode(b"daniel:datascientest").decode('utf-8')
    print_info(f"Credentials encodés: {credentials}")
    
    headers = {
        "Authorization": f"Basic {credentials}"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/user", headers=headers)
        
        if response.status_code == 200:
            print_success(f"Status {response.status_code}")
            print(f"Response: {response.text}")
        else:
            print_error(f"Status {response.status_code}")
            
    except Exception as e:
        print_error(f"Erreur: {e}")


def test_decode_intercepted_request():
    """Test: Démonstration du danger - décoder un token intercepté"""
    print_test("TEST 8: Sécurité - Décoder un token intercepté")
    
    # Simuler une requête interceptée
    intercepted_tokens = {
        "daniel": "ZGFuaWVsOmRhdGFzY2llbnRlc3Q=",
        "john": "am9objpzZWNyZXQ="
    }
    
    print_info("  DÉMONSTRATION: Base64 n'est PAS sécurisé !")
    print()
    
    for user, token in intercepted_tokens.items():
        decoded = base64.b64decode(token).decode('utf-8')
        username, password = decoded.split(':')
        
        print(f"Token intercepté: {token}")
        print(f"  → Décodé en 1 seconde: {username}:{password}")
        print(f"  → Username: {username}")
        print(f"  → Password: {RED}{password}{RESET}")
        print()
    
    print_info(" Solution: Toujours utiliser HTTPS en production !")


def demo_base64_encoding():
    """Démonstration de l'encodage Base64"""
    print_test("DEMO: Encodage/Décodage Base64")
    
    examples = [
        ("daniel", "datascientest"),
        ("john", "secret"),
        ("alice", "wonderland")
    ]
    
    for username, password in examples:
        credentials = f"{username}:{password}"
        encoded = base64.b64encode(credentials.encode()).decode()
        decoded = base64.b64decode(encoded).decode()
        
        print(f"\nOriginal:  {credentials}")
        print(f"Encodé:    {encoded}")
        print(f"Décodé:    {decoded}")
        print(f"Header:    Authorization: Basic {encoded}")


def test_all_endpoints():
    """Test: Tous les endpoints"""
    print_test("TEST 9: Résumé de tous les endpoints")
    
    endpoints = [
        ("/", "GET", False, "Route publique"),
        ("/user", "GET", True, "Message de bienvenue"),
        ("/me", "GET", True, "Informations utilisateur"),
        ("/docs", "GET", False, "Documentation Swagger"),
        ("/redoc", "GET", False, "Documentation ReDoc"),
    ]
    
    print(f"\n{'Endpoint':<15} {'Méthode':<8} {'Auth?':<8} {'Description'}")
    print("-" * 70)
    
    for endpoint, method, auth_required, description in endpoints:
        auth_status = " Oui" if auth_required else " Non"
        print(f"{endpoint:<15} {method:<8} {auth_status:<8} {description}")


if __name__ == "__main__":
    print("\n" + "" * 35)
    print("TESTS API FASTAPI HTTP BASIC AUTH")
    print("" * 35)
    
    try:
        # Tests fonctionnels
        test_public_route()
        test_no_auth()
        test_daniel_auth()
        test_john_auth()
        test_wrong_password()
        test_wrong_username()
        test_manual_base64_header()
        
        # Démonstrations
        demo_base64_encoding()
        test_decode_intercepted_request()
        
        # Résumé
        test_all_endpoints()
        
        print_separator()
        print(f"{GREEN} TOUS LES TESTS TERMINÉS{RESET}")
        print_separator()
        print(f"\n{YELLOW} Accédez à la documentation interactive:{RESET}")
        print(f"   • Swagger UI: http://localhost:8000/docs")
        print(f"   • ReDoc:      http://localhost:8000/redoc")
        print()
        
    except requests.exceptions.ConnectionError:
        print(f"\n{RED} ERREUR: Impossible de se connecter à l'API{RESET}")
        print("Assurez-vous que l'API est lancée avec:")
        print(f"  {BLUE}uvicorn fastapi_http_basic:app --reload --port 8000{RESET}")
        print()
