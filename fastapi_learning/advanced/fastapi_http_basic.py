from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext

# Instanciation de l'API FastAPI et de la sécurité HTTP Basic
app = FastAPI()
security = HTTPBasic()
# Utiliser pbkdf2_sha256 au lieu de bcrypt pour éviter les problèmes de compatibilité
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# Hashes pré-calculés pour éviter les problèmes au démarrage
# Ces hashes correspondent respectivement à 'datascientest' et 'secret'
DANIEL_HASH = "$pbkdf2-sha256$29000$yVmLMaY05nwP4bw3Zqw15g$WmPCdALqJFQlK.lxLO5nsZ9Cr4W.f4FEwAMOjsZ9I2c"
JOHN_HASH = "$pbkdf2-sha256$29000$HWMMISSkFEKode6dk7L2/g$Q6j0Dbk4cgFV0eB5PIW6mcQbBibnuMHAy9Qg1WfzW04"

# Base de données des utilisateurs avec mots de passe hachés
users = {
    "daniel": {
        "username": "daniel",
        "name": "Daniel Datascientest",
        "hashed_password": DANIEL_HASH,
    },
    "john": {
        "username": "john",
        "name": "John Datascientest",
        "hashed_password": JOHN_HASH,
    }
}


def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Vérifie les credentials de l'utilisateur et retourne le username si valide.
    
    Cette fonction est utilisée comme dépendance pour les routes protégées.
    Elle récupère les credentials via HTTPBasicCredentials et vérifie :
    1. Si l'utilisateur existe dans la base de données
    2. Si le mot de passe correspond au hash stocké
    
    Args:
        credentials (HTTPBasicCredentials): Les credentials fournis par le client
            - credentials.username : nom d'utilisateur
            - credentials.password : mot de passe en clair
    
    Returns:
        str: Le nom d'utilisateur si l'authentification réussit
    
    Raises:
        HTTPException 401: Si les credentials sont incorrects
            - Headers: WWW-Authenticate: Basic (pour déclencher la popup navigateur)
    """
    username = credentials.username
    
    # Vérifier si l'utilisateur existe et si le mot de passe correspond
    if not(users.get(username)) or not(pwd_context.verify(credentials.password, users[username]['hashed_password'])):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    return credentials.username


@app.get("/user")
def current_user(username: str = Depends(get_current_user)):
    """
    Route protégée retournant un message de bienvenue personnalisé.
    
    Description:
    Cette route renvoie un message de bienvenue personnalisé en utilisant 
    le nom d'utilisateur fourni en tant que dépendance.

    Args:
        username (str, dépendance): Le nom d'utilisateur récupéré à partir 
                                     de la dépendance `get_current_user`.

    Returns:
        str: Un message de bienvenue personnalisé avec le nom d'utilisateur.

    Raises:
        HTTPException 401: Si la dépendance `get_current_user` échoue 
                           (credentials invalides)
    
    Exemples:
        curl -u daniel:datascientest http://localhost:8000/user
        # Retourne: "Hello daniel"
    """
    return "Hello {}".format(username)


@app.get("/")
def root():
    """
    Route publique (non protégée) - informations sur l'API.
    
    Returns:
        dict: Informations de base sur l'API
    """
    return {
        "message": "FastAPI HTTP Basic Auth API",
        "endpoints": {
            "/user": "Protected route - requires authentication",
            "/docs": "Swagger UI documentation",
            "/redoc": "ReDoc documentation"
        },
        "users": ["daniel", "john"]
    }


@app.get("/me")
def read_current_user(username: str = Depends(get_current_user)):
    """
    Route protégée retournant les informations complètes de l'utilisateur.
    
    Args:
        username (str, dépendance): Nom d'utilisateur authentifié
    
    Returns:
        dict: Informations de l'utilisateur (sans le mot de passe)
    """
    user_data = users[username].copy()
    # Ne jamais exposer le hash du mot de passe !
    user_data.pop('hashed_password', None)
    return user_data


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
