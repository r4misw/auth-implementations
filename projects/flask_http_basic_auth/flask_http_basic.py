from flask import Flask
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

# Instanciation de l'API Flask et de l'authentification HTTP Basic
api = Flask(import_name='my_api')
auth = HTTPBasicAuth()

# Base de données des utilisateurs avec mots de passe hachés
users = {
    "daniel": {
        'password': generate_password_hash("datascientest"),
        'private': 'Private Resource Daniel',
        'role': ['admin', 'user']
    },
    "john": {
        'password': generate_password_hash("secret"),
        'private': 'Private Resource John',
        'role': 'user'
    }
}


@auth.verify_password
def verify_password(username, password):
    """
    Vérifie les informations d'identification de l'utilisateur.
    
    Args:
        username (str): Le nom d'utilisateur fourni
        password (str): Le mot de passe en clair fourni
    
    Returns:
        str or None: Le nom d'utilisateur si les credentials sont valides, None sinon
    """
    if username in users and check_password_hash(users.get(username)['password'], password):
        return username


@auth.get_user_roles
def get_user_roles(user):
    """
    Récupère les rôles d'un utilisateur.
    
    Args:
        user (str): Le nom d'utilisateur
    
    Returns:
        list or str: La liste des rôles de l'utilisateur
    """
    return users.get(user)['role']


@api.route('/admin')
@auth.login_required(role='admin')
def admin():
    """
    Route accessible uniquement par les administrateurs.
    
    Description:
    Cette route est accessible uniquement par les utilisateurs ayant le rôle 'admin'. 
    Elle affiche un message de bienvenue spécifique aux administrateurs.

    Args:
    Aucun argument requis.

    Returns:
    - str: Un message de bienvenue pour l'administrateur actuellement authentifié.

    Raises:
    - HTTPException(401, detail="Unauthorized"): Si l'utilisateur n'est pas authentifié 
      ou n'a pas le rôle 'admin', une exception HTTP 401 Unauthorized est levée.
    """
    return "Hello {}, vous êtes admin!".format(auth.current_user())


@api.route('/')
@auth.login_required(role='user')
def index():
    """
    Route accessible par les utilisateurs authentifiés avec le rôle 'user'.
    
    Description:
    Cette route est accessible uniquement par les utilisateurs ayant le rôle 'user'. 
    Elle affiche un message de bienvenue générique.

    Args:
    Aucun argument requis.

    Returns:
    - str: Un message de bienvenue pour l'utilisateur actuellement authentifié.

    Raises:
    - HTTPException(401, detail="Unauthorized"): Si l'utilisateur n'est pas authentifié 
      ou n'a pas le rôle 'user', une exception HTTP 401 Unauthorized est levée.
    """
    return "Hello, {}!".format(auth.current_user())


@api.route('/private')
@auth.login_required(role='user')
def private():
    """
    Route privée affichant les ressources personnelles de l'utilisateur.
    
    Description:
    Cette route est accessible uniquement par les utilisateurs ayant le rôle 'user'. 
    Elle affiche des informations privées de l'utilisateur.

    Args:
    Aucun argument requis.

    Returns:
    - str: Les informations privées de l'utilisateur actuellement authentifié.

    Raises:
    - HTTPException(401, detail="Unauthorized"): Si l'utilisateur n'est pas authentifié 
      ou n'a pas le rôle 'user', une exception HTTP 401 Unauthorized est levée.
    """
    return "Resource : {}".format(users[auth.current_user()]['private'])


if __name__ == '__main__':
    api.run(debug=True, host='0.0.0.0', port=5000)
