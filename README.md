# Ma Collection — Cuisine & Recettes

Application complète (API + Web) permettant de parcourir un catalogue de recettes de cuisine et de gérer sa collection personnelle (statut, note, commentaire).

## Stack technique
- **Backend** : Python, FastAPI, SQLModel, PostgreSQL (asyncpg), JWT (bcrypt)
- **Frontend** : React 18, TypeScript (mode strict), Vite

## Prérequis
- Python 3.10 à 3.12 (développé et testé avec 3.10)
- Node.js 18 ou plus (version LTS)
- PostgreSQL 14 ou plus

## 1. Base de données PostgreSQL

### Windows
1. Installez PostgreSQL depuis https://www.postgresql.org/download/windows/ et notez le mot de passe choisi pour le compte `postgres`.
2. Lancez **SQL Shell (psql)** depuis le menu Démarrer. Appuyez sur Entrée pour accepter les valeurs par défaut (serveur, base, port, utilisateur), puis saisissez le mot de passe.

### Linux / macOS
```bash
sudo -u postgres psql
```
(le service PostgreSQL doit être démarré)

### Création de la base (toutes plateformes)
Dans l'invite `psql`, tapez :

```sql
CREATE USER ma_collection_user WITH PASSWORD 'votre_mot_de_passe';
CREATE DATABASE ma_collection OWNER ma_collection_user;
\q
```

Choisissez un mot de passe composé uniquement de lettres et de chiffres : certains caractères (`#`, `@`, `:`, `/`) cassent l'URL de connexion.

## 2. Backend (API)

### Windows (PowerShell)
```powershell
cd api
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```
Si `py` n'est pas reconnu, utilisez `python`. Si PowerShell refuse d'activer l'environnement, ouvrez plutôt l'invite de commandes (`cmd`) et remplacez la troisième ligne par `.venv\Scripts\activate.bat`.

### Linux / macOS
```bash
cd api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### Configuration
Éditez le fichier `api/.env` (`notepad .env` sous Windows) :
- `DATABASE_URL=postgresql+asyncpg://ma_collection_user:VOTRE_MOT_DE_PASSE@localhost:5432/ma_collection`
- `JWT_SECRET_KEY` : générez une clé avec la commande ci-dessous et collez le résultat

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Peuplement et lancement
Peuplez le catalogue (40 recettes, relançable sans créer de doublons) :

```bash
python -m app.seed
```

Démarrez l'API (laissez ce terminal ouvert) :

```bash
python -m uvicorn app.main:app --reload
```

L'API est disponible sur http://localhost:8000, documentation interactive sur http://localhost:8000/docs.

## 3. Frontend (Web)

Dans un **second terminal** :

```bash
cd web
npm install
npm run dev
```

Le site est disponible sur http://localhost:5173. L'API doit tourner en même temps.

## Utilisation
1. Ouvrez http://localhost:5173
2. Créez un compte via « Connexion » puis « Pas encore de compte ? S'inscrire »
3. Parcourez le catalogue, consultez une fiche recette, ajoutez-la à votre collection
4. Gérez votre collection (statut, note, suppression) et consultez vos statistiques

## Dépannage
- **Erreur d'authentification PostgreSQL** : vérifiez le mot de passe dans `DATABASE_URL` (lettres et chiffres uniquement) et que PostgreSQL est démarré.
- **Catalogue vide ou « Impossible de charger »** : vérifiez que l'API tourne, et que `python -m app.seed` a été exécuté.
- **Port 8000 ou 5173 déjà utilisé** : fermez l'ancien serveur, ou arrêtez-le avec Ctrl+C.

## Sécurité
- Mots de passe hachés avec bcrypt (jamais stockés ni exposés en clair)
- Authentification par JWT (expiration 30 min)
- CORS restreint à une liste blanche d'origines
- Toute action sur la collection est vérifiée côté serveur (un utilisateur ne peut accéder qu'à ses propres entrées)
- Aucun secret dans le dépôt : le fichier `.env` est ignoré par Git