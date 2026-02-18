# Exercice Pratique: Vérification de Signature et Déchiffrement

## Contexte

Clementine a reçu deux fichiers :
- `encrypted_message_for_clementine` : Un message chiffré
- `signature_for_clementine.txt` : La signature du message

Objectif : Découvrir le contenu du message et l'identité de l'expéditeur.

---

## Solution

### Étape 1: Télécharger les fichiers

```bash
wget https://dst-de.s3.eu-west-3.amazonaws.com/api_security_theory_en/keys/signature_for_clementine.txt
wget https://dst-de.s3.eu-west-3.amazonaws.com/api_security_theory_en/keys/encrypted_message_for_clementine
wget https://dst-de.s3.eu-west-3.amazonaws.com/api_security_theory_en/keys/clementine_private.key
wget https://dst-de.s3.eu-west-3.amazonaws.com/api_security_theory_en/keys/alice_public.key
wget https://dst-de.s3.eu-west-3.amazonaws.com/api_security_theory_en/keys/bob_public.key
```

### Étape 2: Déchiffrer le message

Clementine utilise sa clé privée pour déchiffrer le message :

```bash
openssl rsautl -decrypt -inkey clementine_private.key -in encrypted_message_for_clementine
```

**Résultat :**
```
Hi Clementine! How are you ?
```

**Explication :** Seul Clementine peut déchiffrer ce message car seule sa clé privée peut ouvrir un message chiffré avec sa clé publique.

---

### Étape 3: Vérifier l'identité de l'expéditeur

Clementine reçoit la signature. Pour vérifier qui l'a envoyée, elle doit essayer avec les clés publiques connues.

**Essayer avec Alice :**
```bash
openssl rsautl -verify -pubin -inkey alice_public.key -in signature_for_clementine.txt
```

**Résultat :** Erreur - Ce n'est pas Alice

**Essayer avec Bob :**
```bash
openssl rsautl -verify -pubin -inkey bob_public.key -in signature_for_clementine.txt
```

**Résultat :**
```
b5404d66b4a9c397acc77495316619c1  message_to_clementine.txt
```

**Conclusion :** La signature a été créée avec la clé privée de Bob. Bob est donc l'expéditeur !

---

## Concepts Clés Démontrés

| Concept | Démonstration |
|---------|---------------|
| **Chiffrement asymétrique** | Seul Clementine peut déchiffrer (sa clé privée) |
| **Signature numérique** | Bob prouve son identité avec sa clé privée |
| **Vérification** | N'importe qui avec la clé publique de Bob peut vérifier |
| **Authentification** | Impossible de nier avoir envoyé le message |
| **Intégrité** | Il y a preuve que c'est le message exact de Bob |

---

## Application dans le Monde Réel

### Emails Signés

```
De: bob@example.com
À: clementine@example.com
Sujet: Réunion demain

Message signé numériquement avec la clé privée de Bob
```

Clementine peut vérifier que c'est vraiment Bob qui a envoyé ce mail.

### Certificats SSL/TLS

```
Serveur HTTPS envoie :
  - Son certificat (clé publique)
  - Signé par Let's Encrypt (CA)

Client vérifie :
  - La signature de Let's Encrypt
  - Que le certificat n'est pas expiré
  - Que le domaine correspond
```

---

## Chiffrement Symétrique vs Asymétrique

**Asymétrique (ce que nous avons fait) :**
- Message chiffré avec clé publique
- Déchiffré seulement avec clé privée
- Utilisé pour authentification et échange de clés

**En Production (HTTPS) :**
1. **Handshake TLS (Asymétrique)** : Établir connexion sécurisée
2. **Échange de clés** : Créer une clé symétrique
3. **Communication (Symétrique)** : Chiffrer les données rapides

```
Client --[Asymétrique]--> Serveur
        Négociation
        création clé_session

Client <--[Symétrique]--> Serveur
        clé_session
        Données chiffrées rapides
```

---

## Points à Retenir

1. Un message chiffré avec la clé publique ne peut être déchiffré que avec la clé privée correspondante
2. Une signature créée avec la clé privée peut être vérifiée par toute personne ayant la clé publique
3. Cela garantit à la fois confidentialité (chiffrement) et authentification (signature)
4. HTTPS utilise cette combinaison pour sécuriser Internet

---

## Pour Aller Plus Loin

### Générer Votre Propre Paire de Clés

```bash
# Générer une clé privée RSA 2048 bits
openssl genrsa -out my_private.key 2048

# Extraire la clé publique
openssl rsa -in my_private.key -pubout -out my_public.key
```

### Signer Vos Propres Messages

```bash
# Signer un message
openssl rsautl -sign -inkey my_private.key -in message.txt -out message.sig

# Vérifier la signature
openssl rsautl -verify -pubin -inkey my_public.key -in message.sig
```

### Créer Un Certificat Auto-Signé

```bash
# Générateur un certificat valide 365 jours
openssl req -x509 -newkey rsa:4096 -nodes \
  -keyout key.pem -out cert.pem -days 365
```

---

## Intégration avec Votre API

Dans votre API d'authentification (fichier `SECURITY.md`), les concepts appliqués sont :

- **OAuth 2.0** : Token JWT signé avec clé privée
- **Client** : Vérifie la signature avec clé publique
- **HTTPS** : Utilise certificat X.509 fourni par Let's Encrypt
- **Handshake TLS** : Automatique lors de la connexion HTTPS

```python
# Exemple JWT signé (asymétrique ou symétrique)
import jwt

# Signer un token
token = jwt.encode(
    {"user_id": 123},
    "secret_key",
    algorithm="HS256"
)

# Vérifier le token
decoded = jwt.decode(token, "secret_key", algorithms=["HS256"])
```
