"""
FastAPI JWT Authentication

Ce fichier implémente une authentification JWT (JSON Web Tokens) avec FastAPI.

Utilisateurs de test:
- daniel / datascientest
- john / secret

Routes:
- GET  /              - Route publique
- GET  /secured       - Route protégée par JWT
- POST /user/signup   - Inscription (crée un token)
- POST /user/login    - Connexion (retourne un token)

Pour tester:
    uvicorn fastapi_jwt:api --reload --port 8001
"""

from fastapi import Request, HTTPException, Body, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from fastapi import FastAPI
import time
import jwt

# Configuration JWT
JWT_SECRET = "edc30d44e02ebfc88f2ea5060aef05d4a6f028f284d8d9f4cd3b2d03c195af09"  # Même clé que Flask JWT
JWT_ALGORITHM = "HS256"
TOKEN_EXPIRATION = 600  # 10 minutes (600 secondes)

# Base de données utilisateurs (en mémoire)
users = []


class UserSchema(BaseModel):
    """Modèle pour les données utilisateur"""
    username: str
    password: str


def check_user(data: UserSchema):
    """
    Vérifie si les credentials d'un utilisateur sont valides
    
    Args:
        data (UserSchema): Données utilisateur (username + password)
    
    Returns:
        bool: True si l'utilisateur existe et le mot de passe est correct
    """
    for user in users:
        if user.username == data.username and user.password == data.password:
            return True
    return False


def token_response(token: str):
    """
    Formate la réponse contenant le token
    
    Args:
        token (str): Le token JWT
    
    Returns:
        dict: Dictionnaire avec la clé 'access_token'
    """
    return {"access_token": token}


def sign_jwt(user_id: str):
    """
    Crée un token JWT pour un utilisateur
    
    Args:
        user_id (str): L'identifiant de l'utilisateur (username)
    
    Returns:
        dict: Réponse contenant le token JWT
    """
    payload = {
        "user_id": user_id,
        "expires": time.time() + TOKEN_EXPIRATION
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)


def decode_jwt(token: str):
    """
    Décode et valide un token JWT
    
    Args:
        token (str): Le token JWT à décoder
    
    Returns:
        dict or None: Le payload décodé si valide, None si expiré, {} si erreur
    """
    try:
        decoded_token = jwt.decode(
            token, JWT_SECRET, algorithms=[JWT_ALGORITHM]
        )
        # Vérifie l'expiration
        return (
            decoded_token if decoded_token["expires"] >= time.time() else None
        )
    except Exception:
        return {}


class JWTBearer(HTTPBearer):
    """
    Classe de dépendance pour protéger les routes avec JWT
    
    Vérifie:
    - Que l'en-tête Authorization est présent
    - Que le schéma est 'Bearer'
    - Que le token est valide et non expiré
    """
    
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403,
                    detail="Invalid authentication scheme."
                )
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403,
                    detail="Invalid token or expired token."
                )
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=403,
                detail="Invalid authorization code."
            )

    def verify_jwt(self, jwtoken: str):
        """
        Vérifie la validité d'un token JWT
        
        Args:
            jwtoken (str): Le token à vérifier
        
        Returns:
            bool: True si le token est valide, False sinon
        """
        isTokenValid: bool = False

        try:
            payload = decode_jwt(jwtoken)
        except Exception:
            payload = None
        
        if payload:
            isTokenValid = True
        
        return isTokenValid


# Création de l'application FastAPI
api = FastAPI(
    title="FastAPI JWT Authentication",
    description="API sécurisée avec JWT (JSON Web Tokens)",
    version="1.0.0"
)


@api.get("/", tags=["root"])
async def read_root():
    """
    Route publique - Accessible sans authentification
    
    Returns:
        dict: Message de bienvenue et informations sur l'API
    """
    return {
        "message": "FastAPI JWT Authentication API",
        "endpoints": {
            "/": "Route publique",
            "/secured": "Route protégée (JWT requis)",
            "/user/signup": "Inscription (POST)",
            "/user/login": "Connexion (POST)"
        },
        "registered_users": len(users),
        "token_expiration": f"{TOKEN_EXPIRATION} seconds ({TOKEN_EXPIRATION/60} minutes)"
    }


@api.get("/secured", dependencies=[Depends(JWTBearer())], tags=["root"])
async def read_root_secured():
    """
    Route protégée - Nécessite un JWT valide
    
    Headers requis:
        Authorization: Bearer <token>
    
    Returns:
        dict: Message de confirmation d'accès sécurisé
    
    Raises:
        HTTPException(403): Si le token est absent, invalide ou expiré
    """
    return {"message": "Hello World! but secured"}


@api.post("/user/signup", tags=["user"])
async def create_user(user: UserSchema = Body(...)):
    """
    Inscription d'un nouvel utilisateur
    
    Crée un compte utilisateur et retourne immédiatement un JWT.
    
    Args:
        user (UserSchema): Données utilisateur (username + password)
    
    Request body example:
        {
            "username": "daniel",
            "password": "datascientest"
        }
    
    Returns:
        dict: Contient le token JWT dans 'access_token'
    
    Example:
        {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        }
    """
    users.append(user)
    return sign_jwt(user.username)


@api.post("/user/login", tags=["user"])
async def user_login(user: UserSchema = Body(...)):
    """
    Connexion d'un utilisateur existant
    
    Vérifie les credentials et retourne un JWT si valides.
    
    Args:
        user (UserSchema): Credentials (username + password)
    
    Request body example:
        {
            "username": "daniel",
            "password": "datascientest"
        }
    
    Returns:
        dict: Contient le token JWT si succès, message d'erreur sinon
    
    Example (succès):
        {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        }
    
    Example (échec):
        {
            "error": "Wrong login details!"
        }
    """
    if check_user(user):
        return sign_jwt(user.username)  # FIX: était user.email (erreur dans le cours)
    return {"error": "Wrong login details!"}


if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print(" FASTAPI JWT AUTHENTICATION")
    print("=" * 60)
    print(" URL: http://127.0.0.1:8001")
    print(" Docs: http://127.0.0.1:8001/docs")
    print(" ReDoc: http://127.0.0.1:8001/redoc")
    print("=" * 60)
    print("\n Pour tester:")
    print("1. Inscription: POST /user/signup")
    print("2. Connexion:   POST /user/login")
    print("3. Route sécurisée: GET /secured (avec token)")
    print("\n⌨  Ctrl+C pour arrêter\n")
    print("=" * 60)
    
    uvicorn.run(api, host="127.0.0.1", port=8001)
