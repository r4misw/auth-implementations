"""
FastAPI OAuth 2.0 Authentication

Ce fichier implémente OAuth 2.0 (Open Authorization) avec FastAPI.
OAuth 2.0 est le standard moderne pour l'autorisation et l'authentification.

Flux OAuth 2.0 Password:
1. Client envoie username + password à /token
2. Serveur vérifie et retourne un JWT access token
3. Client utilise le token pour accéder aux ressources protégées

Utilisateurs de test:
- danieldatascientest / datascientest
- johndatascientest / secret

Routes:
- POST /token           - Obtenir un access token (OAuth2)
- GET  /                - Route publique
- GET  /secured         - Route protégée par OAuth2

Pour tester:
    uvicorn fastapi_oauth:app --reload --port 8002
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from typing import Optional
import jwt
from jwt.exceptions import PyJWTError
from datetime import datetime, timedelta

# Configuration de l'application
app = FastAPI(
    title="FastAPI OAuth 2.0 Authentication",
    description="API sécurisée avec OAuth 2.0 et JWT",
    version="1.0.0"
)

# Configuration du hashage de mots de passe (pbkdf2_sha256)
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# Configuration OAuth2
# tokenUrl="token" indique où le client doit envoyer les credentials
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Configuration JWT
SECRET_KEY = "edc30d44e02ebfc88f2ea5060aef05d4a6f028f284d8d9f4cd3b2d03c195af09"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRATION = 30  # minutes


# Modèles Pydantic
class Token(BaseModel):
    """Modèle pour la réponse token"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Modèle pour les données extraites du token"""
    username: Optional[str] = None


class User(BaseModel):
    """Modèle pour un utilisateur"""
    username: str
    name: str
    email: str
    resource: str


# Base de données utilisateurs (en mémoire)
users_db = {
    "danieldatascientest": {
        "username": "danieldatascientest",
        "name": "Daniel Datascientest",
        "email": "daniel@datascientest.com",
        "hashed_password": pwd_context.hash('datascientest'),
        "resource": "Module DE",
    },
    "johndatascientest": {
        "username": "johndatascientest",
        "name": "John Datascientest",
        "email": "john@datascientest.com",
        "hashed_password": pwd_context.hash('secret'),
        "resource": "Module DS",
    }
}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Vérifie si un mot de passe en clair correspond au hash
    
    Args:
        plain_password: Mot de passe en clair
        hashed_password: Hash bcrypt du mot de passe
    
    Returns:
        bool: True si le mot de passe est correct
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Crée un JWT access token
    
    Args:
        data: Données à encoder dans le token (ex: {"sub": "username"})
        expires_delta: Durée de validité du token
    
    Returns:
        str: Token JWT encodé
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Extrait et valide l'utilisateur depuis le token JWT
    
    Cette fonction est utilisée comme dépendance (Depends) pour protéger les routes.
    
    Args:
        token: Token JWT récupéré automatiquement depuis le header Authorization
    
    Returns:
        dict: Données de l'utilisateur
    
    Raises:
        HTTPException(401): Si le token est invalide ou l'utilisateur n'existe pas
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Décoder le JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise credentials_exception
        
        token_data = TokenData(username=username)
    
    except PyJWTError:
        raise credentials_exception
    
    # Récupérer l'utilisateur depuis la base de données
    user = users_db.get(username, None)
    
    if user is None:
        raise credentials_exception
    
    return user


# ============================================
# ROUTES
# ============================================

@app.post("/token", response_model=Token, tags=["authentication"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Route OAuth 2.0 pour obtenir un access token
    
     IMPORTANT: Utilise form-data, PAS JSON !
    
    OAuth2PasswordRequestForm attend:
    - username (form field)
    - password (form field)
    - scope (optionnel)
    - client_id (optionnel)
    - client_secret (optionnel)
    
    Args:
        form_data: Données du formulaire OAuth2 (username + password)
    
    Returns:
        Token: access_token et token_type ("bearer")
    
    Raises:
        HTTPException(400): Si username ou password incorrect
    
    Example:
        curl -X POST http://127.0.0.1:8002/token \
          -d "username=danieldatascientest" \
          -d "password=datascientest"
    """
    # Chercher l'utilisateur
    user = users_db.get(form_data.username)
    
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password"
        )
    
    # Vérifier le mot de passe
    hashed_password = user.get("hashed_password")
    
    if not verify_password(form_data.password, hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password"
        )
    
    # Créer le token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRATION)
    access_token = create_access_token(
        data={"sub": form_data.username},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@app.get("/", tags=["public"])
def read_public_data():
    """
    Route publique - Accessible sans authentification
    
    Returns:
        dict: Message de bienvenue et informations API
    """
    return {
        "message": "FastAPI OAuth 2.0 Authentication API",
        "endpoints": {
            "/": "Route publique",
            "/token": "Obtenir un access token (POST, form-data)",
            "/secured": "Route protégée (GET, Bearer token requis)"
        },
        "users": list(users_db.keys()),
        "token_expiration": f"{ACCESS_TOKEN_EXPIRATION} minutes",
        "auth_type": "OAuth 2.0 Password Flow + JWT"
    }


@app.get("/secured", tags=["protected"])
def read_private_data(current_user: dict = Depends(get_current_user)):
    """
    Route protégée - Nécessite un access token OAuth2 valide
    
    Cette route utilise get_current_user comme dépendance pour vérifier
    que l'utilisateur est authentifié.
    
    Args:
        current_user: Utilisateur extrait du token (injecté automatiquement)
    
    Returns:
        dict: Message sécurisé + informations utilisateur
    
    Raises:
        HTTPException(401): Si le token est absent, invalide ou expiré
    
    Example:
        curl -H "Authorization: Bearer <token>" \
          http://127.0.0.1:8002/secured
    """
    return {
        "message": "Hello World, but secured!",
        "user": {
            "username": current_user["username"],
            "name": current_user["name"],
            "email": current_user["email"],
            "resource": current_user["resource"]
        }
    }


@app.get("/me", tags=["protected"])
def read_users_me(current_user: dict = Depends(get_current_user)):
    """
    Route protégée - Retourne les informations de l'utilisateur connecté
    
    Args:
        current_user: Utilisateur extrait du token
    
    Returns:
        User: Informations complètes de l'utilisateur
    """
    return User(
        username=current_user["username"],
        name=current_user["name"],
        email=current_user["email"],
        resource=current_user["resource"]
    )


if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print(" FASTAPI OAUTH 2.0 AUTHENTICATION")
    print("=" * 60)
    print(" URL: http://127.0.0.1:8002")
    print(" Docs: http://127.0.0.1:8002/docs")
    print(" ReDoc: http://127.0.0.1:8002/redoc")
    print("=" * 60)
    print("\n Pour tester:")
    print("1. Obtenir token: POST /token (form-data)")
    print("2. Utiliser token: GET /secured (Bearer token)")
    print("3. Cliquer sur 'Authorize' dans Swagger UI")
    print("\n  IMPORTANT: /token utilise FORM-DATA, pas JSON!")
    print("\n⌨  Ctrl+C pour arrêter\n")
    print("=" * 60)
    
    uvicorn.run(app, host="127.0.0.1", port=8002)
