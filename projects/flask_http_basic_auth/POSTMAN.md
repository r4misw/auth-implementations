# Configuration Postman pour Flask HTTP Basic Auth

## Configuration de Base

**Base URL:** `http://localhost:5000`

## Requêtes à créer dans Postman

### 1. Test sans authentification (401)

**Method:** GET 
**URL:** `http://localhost:5000/` 
**Auth:** No Auth 
**Résultat attendu:** 401 Unauthorized

---

### 2. Route Index avec daniel

**Method:** GET 
**URL:** `http://localhost:5000/` 
**Auth:**
- Type: Basic Auth
- Username: `daniel`
- Password: `datascientest`

**Résultat attendu:** `Hello, daniel!`

---

### 3. Route Admin avec daniel

**Method:** GET 
**URL:** `http://localhost:5000/admin` 
**Auth:**
- Type: Basic Auth
- Username: `daniel`
- Password: `datascientest`

**Résultat attendu:** `Hello daniel, vous êtes admin!`

---

### 4. Route Private avec daniel

**Method:** GET 
**URL:** `http://localhost:5000/private` 
**Auth:**
- Type: Basic Auth
- Username: `daniel`
- Password: `datascientest`

**Résultat attendu:** `Resource : Private Resource Daniel`

---

### 5. Route Index avec john

**Method:** GET 
**URL:** `http://localhost:5000/` 
**Auth:**
- Type: Basic Auth
- Username: `john`
- Password: `secret`

**Résultat attendu:** `Hello, john!`

---

### 6. Route Admin avec john (ERREUR)

**Method:** GET 
**URL:** `http://localhost:5000/admin` 
**Auth:**
- Type: Basic Auth
- Username: `john`
- Password: `secret`

**Résultat attendu:** 403 Forbidden (john n'est pas admin)

---

### 7. Route Private avec john

**Method:** GET 
**URL:** `http://localhost:5000/private` 
**Auth:**
- Type: Basic Auth
- Username: `john`
- Password: `secret`

**Résultat attendu:** `Resource : Private Resource John`

---

### 8. Test avec Header Authorization manuel

**Method:** GET 
**URL:** `http://localhost:5000/admin` 
**Auth:** No Auth 
**Headers:**
```
Authorization: Basic ZGFuaWVsOmRhdGFzY2llbnRlc3Q=
```

**Note:** `ZGFuaWVsOmRhdGFzY2llbnRlc3Q=` = base64("daniel:datascientest")

---

## Comment configurer Basic Auth dans Postman

1. Ouvrir Postman
2. Créer une nouvelle requête
3. Aller dans l'onglet **Authorization**
4. Sélectionner **Type:** `Basic Auth`
5. Entrer:
   - **Username:** daniel ou john
   - **Password:** datascientest ou secret
6. Postman génère automatiquement le header `Authorization: Basic <base64>`

## Tableau récapitulatif

| Endpoint | daniel (admin) | john (user) |
|-----------|----------------|-------------|
| / | 200 | 200 |
| /admin | 200 | 403 |
| /private | 200 | 200 |

## Vérifier le Header dans Postman

Pour voir le header `Authorization` généré :

1. Aller dans l'onglet **Headers**
2. Cocher "Show auto-generated headers"
3. Vous verrez : `Authorization: Basic <base64-string>`

## Encodage Base64

Pour encoder manuellement :

```bash
# En ligne de commande
echo -n "daniel:datascientest" | base64
# Résultat: ZGFuaWVsOmRhdGFzY2llbnRlc3Q=

echo -n "john:secret" | base64
# Résultat: am9objpzZWNyZXQ=
```

```python
# En Python
import base64
base64.b64encode(b"daniel:datascientest").decode()
# 'ZGFuaWVsOmRhdGFzY2llbnRlc3Q='
```

## Astuce Collection Postman

Créez une **Collection** et utilisez une **Variable** pour l'URL de base :

1. Créer une collection "Flask HTTP Basic Auth"
2. Ajouter une variable : `base_url = http://localhost:5000`
3. Dans les requêtes, utiliser : `{{base_url}}/admin`

Cela permet de changer facilement l'URL (localhost → production)
