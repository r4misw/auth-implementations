"""
Tests automatisés pour FastAPI OAuth 2.0 Authentication API

Lance l'API avant de tester:
    cd /home/ubuntu/fastapi_learning/advanced
    source /home/ubuntu/venv/bin/activate
    python3 fastapi_oauth.py

Puis lance les tests:
    python3 test_fastapi_oauth.py
"""

import requests
import json
import jwt
from datetime import datetime
from colorama import Fore, Style, init

# Initialiser colorama
init(autoreset=True)

# Configuration
BASE_URL = "http://127.0.0.1:8002"

# Marqueurs et couleurs
SUCCESS = f"{Fore.GREEN}[OK]"
FAIL = f"{Fore.RED}[FAIL]"
INFO = f"{Fore.CYAN}[INFO]"
WARNING = f"{Fore.YELLOW}[WARN]"

# Utilisateurs de test
TEST_USERS = [
    {"username": "danieldatascientest", "password": "datascientest"},
    {"username": "johndatascientest", "password": "secret"}
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
            print(f"Auth type: {data.get('auth_type')}")
            print(f"Users disponibles: {', '.join(data.get('users', []))}")
        else:
            print(f"{FAIL}: Status {response.status_code}")
    
    except Exception as e:
        print(f"{FAIL}: Erreur: {e}")


def test_token_oauth2():
    """Test 2: Obtenir un token via OAuth2 Password Flow"""
    print_header("2: Obtenir token via POST /token (OAuth2)")
    
    tokens = {}
    
    for user in TEST_USERS:
        try:
            #  OAuth2 utilise form-data, PAS JSON!
            response = requests.post(
                f"{BASE_URL}/token",
                data=user  # form-data, pas json=user
            )
            
            if response.status_code == 200:
                data = response.json()
                access_token = data.get("access_token")
                token_type = data.get("token_type")
                
                if access_token and token_type:
                    tokens[user["username"]] = access_token
                    print(f"{SUCCESS}: {user['username']}: Token reçu")
                    print(f"   Type: {token_type}")
                    print(f"   Token (premiers 50 cars): {access_token[:50]}...")
                else:
                    print(f"{FAIL}: {user['username']}: Réponse incomplète")
            else:
                print(f"{FAIL}: {user['username']}: Status {response.status_code}")
                print(f"   {INFO}: {response.json()}")
        
        except Exception as e:
            print(f"{FAIL}: {user['username']}: {e}")
    
    return tokens


def test_token_invalid_credentials():
    """Test 3: Tentative d'obtenir token avec mauvais credentials"""
    print_header("3: Token avec mauvais credentials (400 attendu)")
    
    try:
        response = requests.post(
            f"{BASE_URL}/token",
            data={"username": "hacker", "password": "wrongpass"}
        )
        
        if response.status_code == 400:
            print(f"{SUCCESS}: Credentials rejetés (400)")
            print(f"{INFO}: Message: {response.json().get('detail')}")
        else:
            print(f"{FAIL}: Status inattendu: {response.status_code}")
    
    except Exception as e:
        print(f"{FAIL}: Erreur: {e}")


def test_secured_route_with_token(tokens):
    """Test 4: Accès route sécurisée avec token valide"""
    print_header("4: Route /secured avec token OAuth2")
    
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
                print(f"   User info: {data.get('user', {}).get('name')}")
                print(f"   Resource: {data.get('user', {}).get('resource')}")
            else:
                print(f"{FAIL}: {username}: Status {response.status_code}")
        
        except Exception as e:
            print(f"{FAIL}: {username}: {e}")


def test_secured_route_without_token():
    """Test 5: Tentative d'accès sans token"""
    print_header("5: Route /secured sans token (401 attendu)")
    
    try:
        response = requests.get(f"{BASE_URL}/secured")
        
        if response.status_code == 401:
            print(f"{SUCCESS}: Accès refusé (401)")
            print(f"{INFO}: Message: {response.json().get('detail')}")
        else:
            print(f"{FAIL}: Status inattendu: {response.status_code}")
    
    except Exception as e:
        print(f"{FAIL}: Erreur: {e}")


def test_secured_route_invalid_token():
    """Test 6: Tentative d'accès avec token invalide"""
    print_header("6: Route /secured avec token invalide (401 attendu)")
    
    invalid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.INVALID.TOKEN"
    
    try:
        response = requests.get(
            f"{BASE_URL}/secured",
            headers={"Authorization": f"Bearer {invalid_token}"}
        )
        
        if response.status_code == 401:
            print(f"{SUCCESS}: Token invalide rejeté (401)")
            print(f"{INFO}: Message: {response.json().get('detail')}")
        else:
            print(f"{FAIL}: Status inattendu: {response.status_code}")
    
    except Exception as e:
        print(f"{FAIL}: Erreur: {e}")


def test_me_route(tokens):
    """Test 7: Route /me pour obtenir infos utilisateur"""
    print_header("7: Route /me (informations utilisateur)")
    
    username = TEST_USERS[0]["username"]
    token = tokens.get(username)
    
    if not token:
        print(f"{FAIL}: Pas de token disponible")
        return
    
    try:
        response = requests.get(
            f"{BASE_URL}/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            user = response.json()
            print(f"{SUCCESS}: Informations récupérées")
            print(f"   Username: {user.get('username')}")
            print(f"   Name: {user.get('name')}")
            print(f"   Email: {user.get('email')}")
            print(f"   Resource: {user.get('resource')}")
        else:
            print(f"{FAIL}: Status {response.status_code}")
    
    except Exception as e:
        print(f"{FAIL}: Erreur: {e}")


def test_decode_jwt(tokens):
    """Test 8: Décoder et analyser les JWT OAuth2"""
    print_header("8: Décodage JWT OAuth2")
    
    username = TEST_USERS[0]["username"]
    token = tokens.get(username)
    
    if not token:
        print(f"{FAIL}: Pas de token disponible")
        return
    
    print(f"\n→ Token de {username}:")
    
    try:
        # Décoder sans vérifier la signature
        decoded = jwt.decode(token, options={"verify_signature": False})
        
        sub = decoded.get("sub")
        exp = decoded.get("exp")
        
        print(f"   Subject (sub): {sub}")
        print(f"   Expires timestamp: {exp}")
        
        if exp:
            exp_time = datetime.fromtimestamp(exp)
            now = datetime.now()
            remaining = (exp_time - now).total_seconds() / 60
            
            print(f"   Expires at: {exp_time}")
            print(f"   Temps restant: {remaining:.1f} minutes")
            
            if remaining <= 0:
                print(f"   {WARNING} Token EXPIRÉ!")
            elif remaining < 5:
                print(f"   {WARNING} Token expire bientôt!")
            else:
                print(f"   {Fore.GREEN} Token valide")
        
        print(f"\n   {WARNING} Contenu complet (visible par tous):")
        print(f"   {json.dumps(decoded, indent=4)}")
    
    except Exception as e:
        print(f"{FAIL}: Erreur de décodage: {e}")


def test_oauth2_vs_jwt():
    """Test 9: Comparaison OAuth2 vs JWT simple"""
    print_header("9: Différence OAuth2 vs JWT simple")
    
    print("\n Comparaison:")
    print("\n1. OAuth2 Password Flow (/token):")
    print("   • Envoie: form-data (username + password)")
    print("   • Reçoit: access_token + token_type")
    print("   • Standard: RFC 6749 (OAuth 2.0)")
    print("   • Use case: Applications web, mobile")
    
    print("\n2. JWT simple (/login):")
    print("   • Envoie: JSON (username + password)")
    print("   • Reçoit: access_token uniquement")
    print("   • Standard: RFC 7519 (JWT)")
    print("   • Use case: APIs simples, prototypes")
    
    print(f"\n{INFO} OAuth2 est plus standardisé et flexible!")
    print(f"{INFO} JWT simple est plus léger et direct")


def test_form_vs_json():
    """Test 10: Démonstration form-data vs JSON"""
    print_header("10: OAuth2 form-data vs JSON")
    
    user = TEST_USERS[0]
    
    print("\n→ Test 1: Avec form-data (correct)")
    try:
        response = requests.post(
            f"{BASE_URL}/token",
            data=user  # form-data
        )
        
        if response.status_code == 200:
            print(f"{SUCCESS}: form-data accepté (OAuth2 standard)")
        else:
            print(f"{FAIL}: Erreur avec form-data")
    except Exception as e:
        print(f"{FAIL}: {e}")
    
    print("\n→ Test 2: Avec JSON (incorrect pour OAuth2)")
    try:
        response = requests.post(
            f"{BASE_URL}/token",
            json=user  # JSON
        )
        
        if response.status_code == 422:
            print(f"{SUCCESS}: JSON rejeté comme attendu (422)")
            print(f"{INFO}: OAuth2 exige form-data, pas JSON!")
        elif response.status_code == 200:
            print(f"{WARNING}: JSON accepté (non-standard)")
        else:
            print(f"{INFO}: Status {response.status_code}")
    except Exception as e:
        print(f"{INFO}: {e}")


def main():
    """Lance tous les tests"""
    print("\n")
    print("" * 35)
    print("TESTS API FASTAPI OAUTH 2.0 AUTHENTICATION")
    print("" * 35)
    
    # Tests
    test_public_route()
    
    # OAuth2 token
    tokens = test_token_oauth2()
    
    if not tokens:
        print(f"\n{FAIL}: Impossible de continuer sans tokens")
        return
    
    # Tests avec credentials invalides
    test_token_invalid_credentials()
    
    # Routes protégées
    test_secured_route_with_token(tokens)
    test_secured_route_without_token()
    test_secured_route_invalid_token()
    
    # Route /me
    test_me_route(tokens)
    
    # Analyse JWT
    test_decode_jwt(tokens)
    
    # Comparaisons
    test_oauth2_vs_jwt()
    test_form_vs_json()
    
    # Résumé
    print("\n" + "=" * 70)
    print(f"{Fore.GREEN} TOUS LES TESTS TERMINÉS")
    print("=" * 70)
    
    print("\n Points clés OAuth 2.0:")
    print("   • Standard moderne pour l'authentification")
    print("   • Utilise form-data (pas JSON) pour /token")
    print("   • Retourne access_token + token_type")
    print("   • JWT utilisé comme format de token")
    print("   • Support natif dans FastAPI")
    print("   • Bouton 'Authorize' dans Swagger UI")
    print()


if __name__ == "__main__":
    main()
