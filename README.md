# Ma Collection : Cuisine & Recettes

Un site de recettes : on parcourt un catalogue de 40 recettes, on se crée un compte, et on range ses recettes dans sa collection personnelle (à découvrir, en cours, terminé, avec une note).

Ce guide est écrit pour **Windows** et pour quelqu'un qui n'a jamais utilisé de terminal. Comptez environ 20 minutes, téléchargements compris.

## À savoir avant de commencer

- Un **terminal** est une fenêtre noire dans laquelle on tape des commandes. Ici, vous n'aurez rien à inventer : il suffit de **copier-coller** les blocs gris, un par un.
- Il faudra **deux fenêtres noires ouvertes en même temps** : une pour l'API (le « cerveau » du site) et une pour le site lui-même. Ne les fermez pas tant que vous utilisez le site.

## Étape 1 : installer 3 programmes

Téléchargez, lancez, puis cliquez sur « Suivant » partout, sauf pour les points signalés.

1. **Python**, version 3.11 ou 3.12 : https://www.python.org/downloads/windows/
   Sur la première fenêtre d'installation, **cochez la case « Add python.exe to PATH »** (en bas), puis « Install Now ».
2. **Node.js**, version « LTS » (le bouton vert) : https://nodejs.org
3. **PostgreSQL** (la base de données) : https://www.postgresql.org/download/windows/
   Pendant l'installation, on vous demande un **mot de passe** pour le compte « postgres ». Choisissez-en un et **notez-le**. Laissez le port `5432`. À la fin, vous pouvez décocher « Stack Builder ».

## Étape 2 : décompresser le projet

Clic droit sur le fichier `.zip` → **Extraire tout…** → **Extraire**.
Ouvrez le dossier obtenu : vous devez voir deux dossiers, `api` et `web`.

## Étape 3 : créer la base de données

1. Appuyez sur la touche Windows, tapez **SQL Shell**, ouvrez **SQL Shell (psql)**.
2. La fenêtre pose quatre questions (Server, Database, Port, Username) : appuyez sur **Entrée** quatre fois.
3. Elle demande le mot de passe de l'étape 1 : tapez-le, puis Entrée. Rien ne s'affiche pendant la frappe, c'est normal.
4. Quand vous voyez `postgres=#`, copiez ces 3 lignes, faites un **clic droit** dans la fenêtre pour coller, puis Entrée :

```
CREATE USER ma_collection_user WITH PASSWORD 'collection2026';
CREATE DATABASE ma_collection OWNER ma_collection_user;
\q
```

Vous devez voir `CREATE ROLE` puis `CREATE DATABASE`. La fenêtre se ferme toute seule.

## Étape 4 : lancer l'API (fenêtre noire n°1)

1. Dans l'explorateur de fichiers, ouvrez le dossier **`api`**.
2. Cliquez dans la **barre d'adresse** en haut (celle qui affiche le chemin du dossier), tapez `cmd` et appuyez sur Entrée. Une fenêtre noire s'ouvre.
3. Copiez-collez ces commandes **une par une**, en attendant la fin de chacune (la deuxième dure 1 à 3 minutes) :

```
py -m venv .venv
```
```
.\.venv\Scripts\python -m pip install -r requirements.txt
```
```
copy .env.example .env
```
```
notepad .env
```

Si Windows répond que `py` n'est pas reconnu, remplacez `py` par `python`.

4. Le Bloc-notes s'ouvre. **Supprimez tout son contenu** (Ctrl+A puis Suppr) et collez ceci :

```
DATABASE_URL=postgresql+asyncpg://ma_collection_user:collection2026@localhost:5432/ma_collection
JWT_SECRET_KEY=COLLEZ_ICI_UNE_CLE
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

Remplacez `COLLEZ_ICI_UNE_CLE` par une longue suite de lettres et de chiffres de votre choix (au moins 32 caractères, par exemple `k8Zp2xQv7LmN4rTa9WcE1yUb5HgD3sJf`). Enregistrez avec Ctrl+S et fermez le Bloc-notes.

5. De retour dans la fenêtre noire, remplissez la base avec les 40 recettes :

```
.\.venv\Scripts\python -m app.seed
```

Vous devez voir : `40 recette(s) ajoutée(s)`.

6. Démarrez l'API :

```
.\.venv\Scripts\python -m uvicorn app.main:app --reload
```

Vous devez voir `Application startup complete`. **Laissez cette fenêtre ouverte** et ne tapez plus rien dedans.

## Étape 5 : lancer le site (fenêtre noire n°2)

1. Dans l'explorateur, ouvrez le dossier **`web`**.
2. Comme à l'étape 4, cliquez dans la barre d'adresse, tapez `cmd`, Entrée.
3. Copiez-collez, une commande à la fois (la première dure 1 à 2 minutes) :

```
npm install
```
```
npm run dev
```

Vous devez voir une ligne `Local: http://localhost:5173/`. **Laissez aussi cette fenêtre ouverte.**

## Étape 6 : utiliser le site

Ouvrez votre navigateur à l'adresse **http://localhost:5173**

1. Cliquez sur **Connexion**, puis sur **Pas encore de compte ? S'inscrire**, et créez votre compte.
2. Parcourez le catalogue (recherche, catégories), ouvrez une recette et ajoutez-la à votre collection.
3. Dans **Ma collection**, changez le statut, donnez une note ou supprimez. La page **Statistiques** résume le tout.

La documentation technique de l'API est visible sur http://localhost:8000/docs

## Arrêter, puis relancer un autre jour

- **Arrêter** : dans chaque fenêtre noire, appuyez sur **Ctrl+C**, puis fermez-la.
- **Relancer** : l'installation n'est pas à refaire. PostgreSQL redémarre tout seul avec Windows. Ouvrez de nouveau une fenêtre noire dans `api` et tapez `.\.venv\Scripts\python -m uvicorn app.main:app --reload`, puis une autre dans `web` avec `npm run dev`.

## Un problème ?

| Message ou symptôme | Que faire |
|---|---|
| `password authentication failed` | Le mot de passe du fichier `.env` n'est pas celui de l'étape 3. Rouvrez-le avec `notepad .env` : il doit contenir `collection2026` dans la ligne `DATABASE_URL`. |
| `connection refused` dans la fenêtre de l'API | PostgreSQL n'est pas démarré. Touche Windows, tapez `services`, ouvrez « Services », cherchez `postgresql-x64-…`, clic droit puis **Démarrer**. |
| Le site affiche « Impossible de charger le catalogue » | L'API n'est pas lancée (étape 4, point 6), ou la base n'a pas été remplie (point 5). |
| `py` ou `npm` « n'est pas reconnu » | Fermez la fenêtre noire et ouvrez-en une nouvelle (les installations ne sont prises en compte que dans les nouvelles fenêtres). Pour `py`, essayez `python`. |
| `address already in use` | Une ancienne fenêtre fait encore tourner le programme : fermez-la. |

## Linux / macOS (pour les habitués du terminal)

```bash
cd api
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env        # puis éditer comme à l'étape 4
.venv/bin/python -m app.seed
.venv/bin/python -m uvicorn app.main:app --reload
```
```bash
cd web && npm install && npm run dev
```

La base se crée avec `sudo -u postgres psql`, puis les mêmes 3 lignes SQL que l'étape 3.

## Informations techniques

- **Backend** : Python, FastAPI (asynchrone), SQLModel, PostgreSQL, authentification JWT, mots de passe hachés avec bcrypt
- **Frontend** : React 18, TypeScript en mode strict, Vite, React Router
- **Sécurité** : secrets hors du dépôt Git (fichier `.env` ignoré), CORS restreint à une liste blanche, vérification côté serveur que chaque utilisateur n'accède qu'à ses propres données