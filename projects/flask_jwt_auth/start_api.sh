#!/bin/bash

# Script de démarrage de l'API Flask JWT

cd "$(dirname "$0")"

echo ""
echo "   FLASK JWT AUTHENTICATION API         "
echo ""
echo ""

# Vérifier si le venv existe
if [ ! -d "venv" ]; then
    echo "  Environnement virtuel non trouvé."
    echo " Création de l'environnement virtuel..."
    python3 -m venv venv
    echo " Environnement créé"
    echo ""
fi

# Activer le venv
echo " Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances si nécessaire
echo " Vérification des dépendances..."
pip list | grep -q Flask
if [ $? -ne 0 ]; then
    echo " Installation des dépendances..."
    pip install -r requirements.txt
    echo " Dépendances installées"
else
    echo " Dépendances déjà installées"
fi

echo ""
echo " Lancement de l'API..."
echo " URL: http://127.0.0.1:5001"
echo " Documentation: README.md"
echo ""
echo "Pour tester:"
echo "  - Route publique:  curl http://127.0.0.1:5001/"
echo "  - Login:           curl -X POST -H 'Content-Type: application/json' -d '{\"username\":\"danieldatascientest\",\"password\":\"datascientest\"}' http://127.0.0.1:5001/login"
echo ""
echo "Pour arrêter: CTRL+C"
echo ""
echo ""

python3 flask_jwt.py
