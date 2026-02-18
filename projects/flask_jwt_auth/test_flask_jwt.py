"""
Tests automatisés pour Flask JWT Authentication
"""

import requests
import json
import jwt as pyjwt
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:5001"

# Couleurs
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
    print(f"{YELLOW}[INFO]{RESET}: {message}")


def test_public_route():
    """Test: Route publique /"""
    print_test("TEST 1: Route publique /")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        
        if response.status_code == 200:
            print_success(f"Status {response.status_code}")
            data = response.json()
            print(f"Message: {data['message']}")
            print(f"Users: {', '.join(data['users'])}")
            print(f"Token expiration: {data['token_expiration']}")
        else:
            print_error(f"Status {response.status_code}")
    except Exception as e:
        print_error(f"Erreur: {e}")


def test_login_success():
    """Test: Login avec credentials valides"""
    print_test("TEST 2: Login avec credentials valides")
    
    credentials = [
        ("danieldatascientest", "datascientest"),
        ("johndatascientest", "secret")
    ]
    
    tokens = {}
    
    for username, password in credentials:
        try:
            response = requests.post(
                f"{BASE_URL}/login",
                json={"username": username, "password": password}
            )
            
            if response.status_code == 200:
                token = response.json()["access_token"]
                tokens[username] = token
                print_success(f"{username}: Token reçu")
                print(f"   Token (premiers 50 cars): {token[:50]}...")
            else:
                print_error(f"{username}: Status {response.status_code}")
        except Exception as e:
            print_error(f"{username}: {e}")
    
    return tokens


def test_login_failure():
    """Test: Login avec mauvais credentials"""
    print_test("TEST 3: Login avec mauvais credentials")
    
    try:
        response = requests.post(
            f"{BASE_URL}/login",
            json={"username": "hacker", "password": "wrongpass"}
        )
        
        if response.status_code == 401:
            print_success(f"Status {response.status_code} (rejeté comme attendu)")
            print_info(f"Message: {response.json()['msg']}")
        else:
            print_error(f"Status {response.status_code} (attendu: 401)")
    except Exception as e:
        print_error(f"Erreur: {e}")


def test_protected_routes_with_token(tokens):
    """Test: Routes protégées avec token valide"""
    print_test("TEST 4: Routes protégées avec token valide")
    
    for username, token in tokens.items():
        print(f"\n{BLUE}→ Utilisateur: {username}{RESET}")
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test route /user
        try:
            response = requests.get(f"{BASE_URL}/user", headers=headers)
            if response.status_code == 200:
                print_success(f"  /user: {response.json()}")
            else:
                print_error(f"  /user: Status {response.status_code}")
        except Exception as e:
            print_error(f"  /user: {e}")
        
        # Test route /resource
        try:
            response = requests.get(f"{BASE_URL}/resource", headers=headers)
            if response.status_code == 200:
                data = response.json()
                print_success(f"  /resource: {data['resource']} (Owner: {data['owner']})")
            else:
                print_error(f"  /resource: Status {response.status_code}")
        except Exception as e:
            print_error(f"  /resource: {e}")


def test_protected_routes_without_token():
    """Test: Routes protégées sans token"""
    print_test("TEST 5: Routes protégées sans token (401 attendu)")
    
    routes = ["/user", "/resource"]
    
    for route in routes:
        try:
            response = requests.get(f"{BASE_URL}{route}")
            
            if response.status_code == 401:
                print_success(f"{route}: Status {response.status_code} (rejeté)")
            else:
                print_error(f"{route}: Status {response.status_code} (attendu: 401)")
        except Exception as e:
            print_error(f"{route}: {e}")


def test_decode_jwt(tokens):
    """Test: Décoder le JWT et afficher son contenu"""
    print_test("TEST 6: Décoder le JWT (sans vérifier la signature)")
    
    for username, token in tokens.items():
        print(f"\n{BLUE}→ Token de {username}:{RESET}")
        
        try:
            # Décoder sans vérifier la signature (juste pour lire le contenu)
            decoded = pyjwt.decode(token, options={"verify_signature": False})
            
            print(f"   Subject (sub): {decoded.get('sub')}")
            print(f"   Token ID (jti): {decoded.get('jti')}")
            print(f"   Type: {decoded.get('type')}")
            print(f"   Fresh: {decoded.get('fresh')}")
            
            # Dates
            iat = decoded.get('iat')
            exp = decoded.get('exp')
            if iat:
                iat_time = datetime.fromtimestamp(iat)
                print(f"   Issued At (iat): {iat_time}")
            if exp:
                exp_time = datetime.fromtimestamp(exp)
                exp_in = (exp_time - datetime.now()).total_seconds() / 60
                print(f"   Expires At (exp): {exp_time}")
                print(f"   Expires in: {exp_in:.1f} minutes")
            
            print(f"\n   {YELLOW}  Contenu complet (visible par tous):{RESET}")
            print(f"   {json.dumps(decoded, indent=4)}")
            
        except Exception as e:
            print_error(f"Erreur décodage: {e}")


def test_jwt_structure(tokens):
    """Test: Analyser la structure du JWT"""
    print_test("TEST 7: Structure du JWT (3 parties)")
    
    # Prendre le premier token
    username = list(tokens.keys())[0]
    token = tokens[username]
    
    parts = token.split('.')
    
    print(f"{BLUE}Token de {username}:{RESET}\n")
    print(f"Token complet ({len(token)} caractères):")
    print(f"{token}\n")
    
    if len(parts) == 3:
        print_success("JWT valide avec 3 parties")
        
        print(f"\n{YELLOW}1. HEADER{RESET} ({len(parts[0])} chars):")
        print(f"   {parts[0]}")
        try:
            import base64
            # Ajouter padding si nécessaire
            header_padded = parts[0] + '=' * (4 - len(parts[0]) % 4)
            header_decoded = base64.urlsafe_b64decode(header_padded)
            print(f"   Décodé: {header_decoded.decode()}")
        except:
            pass
        
        print(f"\n{YELLOW}2. PAYLOAD{RESET} ({len(parts[1])} chars):")
        print(f"   {parts[1][:50]}...")
        
        print(f"\n{YELLOW}3. SIGNATURE{RESET} ({len(parts[2])} chars):")
        print(f"   {parts[2]}")
        print(f"   {YELLOW}  Impossible à falsifier sans la clé secrète !{RESET}")
    else:
        print_error(f"JWT invalide: {len(parts)} partie(s) au lieu de 3")


def demo_jwt_cannot_be_modified(tokens):
    """Démonstration: Impossible de modifier un JWT"""
    print_test("TEST 8: Sécurité - Tentative de modification du JWT")
    
    username = list(tokens.keys())[0]
    token = tokens[username]
    
    print(f"{BLUE}Token original de {username}:{RESET}")
    print(f"{token[:60]}...\n")
    
    # Décoder le payload
    decoded = pyjwt.decode(token, options={"verify_signature": False})
    print(f"Username original: {decoded['sub']}")
    
    # Tenter de modifier (remplacer une lettre)
    modified_token = token[:-10] + "HACKED" + token[-4:]
    
    print(f"\n{YELLOW}Tentative de modification du token...{RESET}")
    print(f"Token modifié: {modified_token[:60]}...")
    
    # Essayer d'utiliser le token modifié
    headers = {"Authorization": f"Bearer {modified_token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/user", headers=headers)
        
        if response.status_code == 422:
            print_success(f" Modification détectée ! Status 422 (Token invalide)")
            print_info("Le serveur a rejeté le token modifié")
        elif response.status_code == 401:
            print_success(f" Modification détectée ! Status 401 (Unauthorized)")
            print_info("La signature ne correspond plus")
        else:
            print_error(f"  Status inattendu: {response.status_code}")
    except Exception as e:
        print_info(f"Erreur (attendue): {e}")
    
    print(f"\n{GREEN} Conclusion: Le JWT est protégé contre les modifications !{RESET}")


if __name__ == "__main__":
    print("\n" + "" * 35)
    print("TESTS API FLASK JWT AUTHENTICATION")
    print("" * 35)
    
    try:
        # Tests
        test_public_route()
        tokens = test_login_success()
        test_login_failure()
        
        if tokens:
            test_protected_routes_with_token(tokens)
            test_protected_routes_without_token()
            test_decode_jwt(tokens)
            test_jwt_structure(tokens)
            demo_jwt_cannot_be_modified(tokens)
        
        print_separator()
        print(f"{GREEN} TOUS LES TESTS TERMINÉS{RESET}")
        print_separator()
        print(f"\n{YELLOW} Points clés:{RESET}")
        print("   • JWT = Header + Payload + Signature")
        print("   • Le contenu est LISIBLE par tous (Base64)")
        print("   • La signature empêche les modifications")
        print("   • Expire automatiquement (30 min)")
        print("   • Utiliser HTTPS en production !")
        print()
        
    except requests.exceptions.ConnectionError:
        print(f"\n{RED} ERREUR: Impossible de se connecter à l'API{RESET}")
        print("Assurez-vous que l'API est lancée avec:")
        print(f"  {BLUE}python flask_jwt.py{RESET}")
        print()
