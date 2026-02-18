"""
Tests automatisés pour FastAPI JWT Authentication API

Lance l'API avant de tester:
    cd /home/ubuntu/fastapi_learning/advanced
    python3 fastapi_jwt.py

Puis lance les tests:
    python3 test_fastapi_jwt.py
"""

import requests
import json
import jwt
from datetime import datetime
from colorama import Fore, Style, init

# Initialiser colorama pour les couleurs dans le terminal
init(autoreset=True)

# Configuration
BASE_URL = "http://127.0.0.1:8001"

# Marqueurs et couleurs
SUCCESS = f"{Fore.GREEN}[OK]"
FAIL = f"{Fore.RED}[FAIL]"
INFO = f"{Fore.CYAN}ℹ  INFO"
WARNING = f"{Fore.YELLOW}  WARNING"

# Utilisateurs de test
TEST_USERS = [
    {"username": "daniel", "password": "datascientest"},
    {"username": "john", "password": "secret"}
]


def print_header(title):
    """Affiche un en-tête de section"""
    print("\n" + "=" * 70)
    print(f"TEST {title}")
    print("=" * 70)


def test_public_route():
    """Test 1: Accès à la route publique"""
    print_header("1: Route publique /")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        
        if response.status_code == 200:
            data = response.json()
            print(f"{SUCCESS}: Status 200")
            print(f"Message: {data.get('message')}")
            print(f"Users enregistrés: {data.get('registered_users')}")
            print(f"Token expiration: {data.get('token_expiration')}")
        else:
            print(f"{FAIL}: Status {response.status_code}")
    
    except Exception as e:
        print(f"{FAIL}: Erreur: {e}")


def test_signup():
    """Test 2: Inscription de nouveaux utilisateurs"""
    print_header("2: Inscription (signup) de nouveaux utilisateurs")
    
    tokens = {}
    
    for user in TEST_USERS:
        try:
            response = requests.post(
                f"{BASE_URL}/user/signup",
                json=user
            )
            
            if response.status_code == 200:
                data = response.json()
                token = data.get("access_token")
                
                if token:
                    tokens[user["username"]] = token
                    print(f"{SUCCESS}: {user['username']}: Token reçu")
                    print(f"   Token (premiers 50 cars): {token[:50]}...")
                else:
                    print(f"{FAIL}: {user['username']}: Pas de token dans la réponse")
            else:
                print(f"{FAIL}: {user['username']}: Status {response.status_code}")
        
        except Exception as e:
            print(f"{FAIL}: {user['username']}: {e}")
    
    return tokens


def test_login():
    """Test 3: Connexion avec credentials valides"""
    print_header("3: Connexion (login) avec credentials valides")
    
    tokens = {}
    
    for user in TEST_USERS:
        try:
            response = requests.post(
                f"{BASE_URL}/user/login",
                json=user
            )
            
            if response.status_code == 200:
                data = response.json()
                token = data.get("access_token")
                
                if token:
                    tokens[user["username"]] = token
                    print(f"{SUCCESS}: {user['username']}: Login réussi")
                    print(f"   Token (premiers 50 cars): {token[:50]}...")
                else:
                    print(f"{FAIL}: {user['username']}: Pas de token")
            else:
                print(f"{FAIL}: {user['username']}: Status {response.status_code}")
        
        except Exception as e:
            print(f"{FAIL}: {user['username']}: {e}")
    
    return tokens


def test_login_invalid():
    """Test 4: Connexion avec mauvais credentials"""
    print_header("4: Connexion avec mauvais credentials")
    
    invalid_user = {"username": "hacker", "password": "wrongpass"}
    
    try:
        response = requests.post(
            f"{BASE_URL}/user/login",
            json=invalid_user
        )
        
        data = response.json()
        
        if "error" in data:
            print(f"{SUCCESS}: Credentials rejetés (comme attendu)")
            print(f"{INFO}: Message: {data['error']}")
        else:
            print(f"{FAIL}: L'API a accepté des credentials invalides!")
    
    except Exception as e:
        print(f"{FAIL}: Erreur: {e}")


def test_secured_route_with_token(tokens):
    """Test 5: Accès à la route sécurisée avec token valide"""
    print_header("5: Route sécurisée /secured avec token valide")
    
    for username, token in tokens.items():
        try:
            response = requests.get(
                f"{BASE_URL}/secured",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"{SUCCESS}: {username}: Accès autorisé")
                print(f"   Message: {data.get('message')}")
            else:
                print(f"{FAIL}: {username}: Status {response.status_code}")
        
        except Exception as e:
            print(f"{FAIL}: {username}: {e}")


def test_secured_route_without_token():
    """Test 6: Tentative d'accès à la route sécurisée sans token"""
    print_header("6: Route sécurisée sans token (403 attendu)")
    
    try:
        response = requests.get(f"{BASE_URL}/secured")
        
        if response.status_code == 403:
            print(f"{SUCCESS}: Accès refusé (403)")
            print(f"{INFO}: Message: {response.json().get('detail')}")
        else:
            print(f"{FAIL}: Status inattendu: {response.status_code}")
    
    except Exception as e:
        print(f"{FAIL}: Erreur: {e}")


def test_secured_route_invalid_token():
    """Test 7: Tentative d'accès avec token invalide"""
    print_header("7: Route sécurisée avec token invalide (403 attendu)")
    
    invalid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.INVALID.TOKEN"
    
    try:
        response = requests.get(
            f"{BASE_URL}/secured",
            headers={"Authorization": f"Bearer {invalid_token}"}
        )
        
        if response.status_code == 403:
            print(f"{SUCCESS}: Token invalide rejeté (403)")
            print(f"{INFO}: Message: {response.json().get('detail')}")
        else:
            print(f"{FAIL}: Status inattendu: {response.status_code}")
    
    except Exception as e:
        print(f"{FAIL}: Erreur: {e}")


def test_decode_jwt(tokens):
    """Test 8: Décoder et analyser les JWT"""
    print_header("8: Décodage et analyse des JWT")
    
    for username, token in tokens.items():
        print(f"\n→ Token de {username}:")
        
        try:
            # Décoder sans vérifier la signature (pour voir le contenu)
            decoded = jwt.decode(token, options={"verify_signature": False})
            
            user_id = decoded.get("user_id")
            expires = decoded.get("expires")
            
            print(f"   User ID: {user_id}")
            print(f"   Expires timestamp: {expires}")
            
            if expires:
                exp_time = datetime.fromtimestamp(expires)
                now = datetime.now()
                remaining = (exp_time - now).total_seconds() / 60
                
                print(f"   Expires at: {exp_time}")
                print(f"   Temps restant: {remaining:.1f} minutes")
                
                if remaining <= 0:
                    print(f"   {WARNING} Token EXPIRÉ!")
                elif remaining < 2:
                    print(f"   {WARNING} Token expire bientôt!")
                else:
                    print(f"   {Fore.GREEN} Token valide")
            
            print(f"\n   {WARNING} Contenu complet (visible par tous):")
            print(f"   {json.dumps(decoded, indent=4)}")
        
        except Exception as e:
            print(f"{FAIL}: Erreur de décodage: {e}")


def test_jwt_structure(tokens):
    """Test 9: Vérifier la structure du JWT"""
    print_header("9: Structure du JWT (3 parties)")
    
    username = TEST_USERS[0]["username"]
    token = tokens.get(username)
    
    if not token:
        print(f"{FAIL}: Pas de token disponible")
        return
    
    print(f"Token de {username}:\n")
    print(f"Token complet ({len(token)} caractères):")
    print(f"{token}\n")
    
    parts = token.split(".")
    
    if len(parts) == 3:
        print(f"{SUCCESS}: JWT valide avec 3 parties\n")
        
        print(f"1. HEADER ({len(parts[0])} chars):")
        print(f"   {parts[0]}")
        
        # Décoder le header (Base64)
        import base64
        try:
            header_decoded = base64.urlsafe_b64decode(parts[0] + "==").decode()
            print(f"   Décodé: {header_decoded}")
        except:
            pass
        
        print(f"\n2. PAYLOAD ({len(parts[1])} chars):")
        print(f"   {parts[1][:50]}...")
        
        print(f"\n3. SIGNATURE ({len(parts[2])} chars):")
        print(f"   {parts[2]}")
        print(f"   {WARNING} Impossible à falsifier sans la clé secrète !")
    else:
        print(f"{FAIL}: JWT invalide, devrait avoir 3 parties séparées par des points")


def test_token_modification(tokens):
    """Test 10: Tentative de modification d'un token"""
    print_header("10: Sécurité - Tentative de modification du JWT")
    
    username = TEST_USERS[0]["username"]
    original_token = tokens.get(username)
    
    if not original_token:
        print(f"{FAIL}: Pas de token disponible")
        return
    
    print(f"Token original de {username}:")
    print(f"{original_token[:50]}...\n")
    
    # Décoder
    decoded = jwt.decode(original_token, options={"verify_signature": False})
    print(f"User ID original: {decoded.get('user_id')}")
    
    # Modifier le payload
    print(f"\nTentative de modification du token...")
    decoded["user_id"] = "hacker"
    
    # Ré-encoder sans la bonne clé
    modified_token = jwt.encode(decoded, "wrong_secret", algorithm="HS256")
    print(f"Token modifié: {modified_token[:50]}...")
    
    # Tenter d'utiliser le token modifié
    try:
        response = requests.get(
            f"{BASE_URL}/secured",
            headers={"Authorization": f"Bearer {modified_token}"}
        )
        
        if response.status_code == 403:
            print(f"{SUCCESS}:  Modification détectée ! Status 403")
            print(f"{INFO}: Le serveur a rejeté le token modifié")
            print(f"\n Conclusion: Le JWT est protégé contre les modifications !")
        else:
            print(f"{FAIL}:   Token modifié accepté (problème de sécurité!)")
    
    except Exception as e:
        print(f"{FAIL}: Erreur: {e}")


def main():
    """Lance tous les tests"""
    print("\n")
    print("" * 35)
    print("TESTS API FASTAPI JWT AUTHENTICATION")
    print("" * 35)
    
    # Tests
    test_public_route()
    
    # Signup (créer les utilisateurs)
    tokens_signup = test_signup()
    
    # Login (récupérer les tokens)
    tokens_login = test_login()
    
    # Test mauvais credentials
    test_login_invalid()
    
    # Utiliser les tokens du login pour la suite
    tokens = tokens_login if tokens_login else tokens_signup
    
    if not tokens:
        print(f"\n{FAIL}: Impossible de continuer sans tokens")
        return
    
    # Routes protégées
    test_secured_route_with_token(tokens)
    test_secured_route_without_token()
    test_secured_route_invalid_token()
    
    # Analyse JWT
    test_decode_jwt(tokens)
    test_jwt_structure(tokens)
    test_token_modification(tokens)
    
    # Résumé
    print("\n" + "=" * 70)
    print(f"{Fore.GREEN} TOUS LES TESTS TERMINÉS")
    print("=" * 70)
    
    print("\n Points clés:")
    print("   • JWT = Header + Payload + Signature")
    print("   • Le contenu est LISIBLE par tous (Base64)")
    print("   • La signature empêche les modifications")
    print("   • Expire automatiquement (10 min)")
    print("   • Utiliser HTTPS en production !")
    print()


if __name__ == "__main__":
    main()
