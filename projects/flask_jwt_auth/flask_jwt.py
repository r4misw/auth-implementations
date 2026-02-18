from flask import Flask
from flask import jsonify
from flask import request
from datetime import timedelta

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from passlib.context import CryptContext

# Configuration du contexte de hachage des mots de passe
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# Base de données des utilisateurs avec mots de passe hachés
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
        'resource': 'Module DS',
    }
}

# Instanciation de l'API Flask
api = Flask(import_name="my_api")

# Configuration JWT
# Clé secrète générée avec: openssl rand -hex 32
api.config["JWT_SECRET_KEY"] = "edc30d44e02ebfc88f2ea5060aef05d4a6f028f284d8d9f4cd3b2d03c195af09"
api.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)

# Initialisation du gestionnaire JWT
jwt = JWTManager(api)


def check_password(plain_password, hashed_password):
    """
    Vérifie si un mot de passe en clair correspond au hash stocké.
    
    Args:
        plain_password (str): Mot de passe en clair fourni par l'utilisateur
        hashed_password (str): Hash du mot de passe stocké en base
    
    Returns:
        bool: True si le mot de passe correspond, False sinon
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_user(database, username):
    """
    Récupère un utilisateur depuis la base de données.
    
    Args:
        database (dict): Base de données des utilisateurs
        username (str): Nom d'utilisateur à rechercher
    
    Returns:
        dict or None: Dictionnaire de l'utilisateur si trouvé, None sinon
    """
    if username in database:
        user_dict = database[username]
        return user_dict


@api.route("/login", methods=["POST"])
def login():
    """
    Route d'authentification pour obtenir un token JWT.
    
    Description:
    Cette route permet à un utilisateur de s'authentifier en fournissant 
    un nom d'utilisateur et un mot de passe. Si l'authentification est 
    réussie, elle renvoie un jeton d'accès JWT.

    Args:
        request.json.get("username", None) (str): Le nom d'utilisateur 
                                                   saisi dans le corps JSON
        request.json.get("password", None) (str): Le mot de passe saisi 
                                                   dans le corps JSON

    Returns:
        JSON: Si l'authentification réussit, renvoie un JSON contenant 
              un jeton d'accès avec une durée de validité de 30 minutes.

    Raises:
        JSONResponse({"msg": "Bad username or password"}, status_code=401): 
            Si l'authentification échoue en raison d'un mauvais nom 
            d'utilisateur ou d'un mot de passe.
    
    Exemple:
        curl -X POST -H "Content-Type: application/json" \\
             -d '{"username":"danieldatascientest", "password":"datascientest"}' \\
             http://127.0.0.1:5000/login
    """
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    
    # Vérifier l'utilisateur et le mot de passe
    user = get_user(users_db, username)
    if not user or not check_password(password, user['hashed_password']):
        return jsonify({"msg": "Bad username or password"}), 401

    # Créer le token JWT avec l'identité de l'utilisateur
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


@api.route("/user", methods=["GET"])
@jwt_required()
def get_current_user():
    """
    Route protégée retournant l'utilisateur actuellement authentifié.
    
    Description:
    Cette route permet de récupérer l'utilisateur actuellement authentifié 
    en utilisant un jeton d'accès JWT.

    Args:
        Aucun argument requis (le JWT est dans le header Authorization).

    Returns:
        JSON: Renvoie un JSON contenant le nom d'utilisateur de l'utilisateur 
              actuellement authentifié.

    Raises:
        Exception JWT: Si la validation du jeton d'accès JWT échoue 
                       (token expiré, invalide, manquant)
    
    Exemple:
        curl -X GET -H 'Authorization: Bearer <votre_token>' \\
             http://127.0.0.1:5000/user
    """
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@api.route("/resource", methods=["GET"])
@jwt_required()
def get_resource():
    """
    Route protégée retournant la ressource associée à l'utilisateur.
    
    Description:
    Cette route permet de récupérer une ressource associée à l'utilisateur 
    actuellement authentifié en utilisant un jeton d'accès JWT.

    Args:
        Aucun argument requis (le JWT est dans le header Authorization).

    Returns:
        JSON: Renvoie un JSON contenant la ressource et le propriétaire 
              de la ressource.

    Raises:
        Exception JWT: Si la validation du jeton d'accès JWT échoue 
                       (token expiré, invalide, manquant)
    
    Exemple:
        curl -X GET -H 'Authorization: Bearer <votre_token>' \\
             http://127.0.0.1:5000/resource
    """
    current_username = get_jwt_identity()
    return jsonify({
        "resource": get_user(users_db, current_username)['resource'],
        "owner": current_username
    })


@api.route("/")
def index():
    """
    Route publique d'information sur l'API.
    
    Returns:
        JSON: Informations sur l'API et les endpoints disponibles
    """
    return jsonify({
        "message": "Flask JWT Authentication API",
        "endpoints": {
            "/login": "POST - Authenticate and get JWT token",
            "/user": "GET - Get current user (requires JWT)",
            "/resource": "GET - Get user resource (requires JWT)"
        },
        "users": ["danieldatascientest", "johndatascientest"],
        "token_expiration": "30 minutes"
    })


if __name__ == "__main__":
    api.run(debug=True, host='0.0.0.0', port=5001)
