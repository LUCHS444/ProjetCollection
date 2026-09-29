# Ma Collection — Cuisine & Recettes

Application complète (API + Web) permettant de parcourir un catalogue de recettes de cuisine et de gérer sa collection personnelle (statut, note, commentaire).

## Stack technique
- **Backend** : Python, FastAPI, SQLModel, PostgreSQL (asyncpg), JWT (bcrypt)
- **Frontend** : React 18, TypeScript (mode strict), Vite

## Prérequis
- Python 3.10+
- Node.js 18+ (installé nativement, pas via un environnement Windows si vous êtes sous WSL)
- PostgreSQL installé et démarré

## Installation et lancement complet

### 1. Base de données PostgreSQL

```bash
sudo apt install -y postgresql postgresql-contrib
sudo service postgresql start
sudo -u postgres psql
```
Dans l'invite psql :
```sql
CREATE DATABASE ma_collection;
CREATE USER ma_collection_user WITH PASSWORD 'votre_mot_de_passe';
GRANT ALL PRIVILEGES ON DATABASE ma_collection TO ma_collection_user;
\q
```

### 2. Backend (API)

```bash
cd api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Éditez `.env` pour renseigner :
- `DATABASE_URL` avec votre mot de passe PostgreSQL
- `JWT_SECRET_KEY` (générez-en une avec `python -c "import secrets; print(secrets.token_hex(32))"`)

Peuplez le catalogue (40 recettes) :
```bash
python -m app.seed
```

Démarrez l'API :
```bash
python -m uvicorn app.main:app --reload
```
L'API est disponible sur `http://localhost:8000`, documentation interactive sur `http://localhost:8000/docs`.

### 3. Frontend (Web)

Dans un second terminal :
```bash
cd web
npm install
npm run dev
```
Le site est disponible sur `http://localhost:5173`.

## Utilisation
1. Ouvrez `http://localhost:5173`
2. Créez un compte via "Connexion" → "Pas encore de compte ? S'inscrire"
3. Parcourez le catalogue, consultez une fiche recette, ajoutez-la à votre collection
4. Gérez votre collection (statut, note, suppression) et consultez vos statistiques

## Sécurité
- Mots de passe hachés avec bcrypt (jamais stockés/exposés en clair)
- Authentification par JWT (expiration 30 min)
- CORS restreint aux origines de développement autorisées
- Toute action sur la collection est vérifiée côté serveur (un utilisateur ne peut accéder qu'à ses propres entrées)