# Ma Collection : Cuisine & Recettes

Un site de recettes : on parcourt un catalogue de 40 recettes, on se crée un compte, et on range ses recettes dans sa collection personnelle (à découvrir, en cours, terminé, avec une note).

Ce guide est écrit pour **Windows** et pour quelqu'un qui n'a jamais utilisé de terminal. Tout se fait dans **Visual Studio Code**. Comptez environ 20 minutes, téléchargements compris.

## À savoir avant de commencer

- Un **terminal** est la zone noire en bas de VS Code, dans laquelle on tape des commandes. Vous n'avez rien à inventer : il suffit de **copier-coller** les blocs gris, **un par un**, en attendant que chacun se termine.
- Il y aura **deux terminaux ouverts en même temps** : un pour l'API (le « cerveau » du site) et un pour le site lui-même. Ne les fermez pas tant que vous utilisez le site.
- Pour coller dans le terminal : **clic droit** dans la zone noire, ou `Ctrl+V`.

## Étape 1 : installer 3 programmes

Téléchargez, lancez, puis cliquez sur « Suivant » partout, sauf pour les points signalés.

1. **Python**, version 3.12 : https://www.python.org/downloads/windows/
   Sur la première fenêtre d'installation, **cochez la case « Add python.exe to PATH »** (en bas), puis « Install Now ».
2. **Node.js**, version « LTS » (le bouton vert) : https://nodejs.org
3. **PostgreSQL** (la base de données) : https://www.postgresql.org/download/windows/
   Pendant l'installation, on vous demande un **mot de passe** pour le compte « postgres ». Choisissez-en un et **notez-le**. Laissez le port `5432`. À la fin, vous pouvez décocher « Stack Builder ».

Après ces installations, **fermez VS Code s'il était ouvert**, pour qu'il prenne en compte les nouveaux programmes.

## Étape 2 : ouvrir le projet dans VS Code

1. Clic droit sur le fichier `.zip` → **Extraire tout…** → **Extraire**.
2. Ouvrez VS Code, puis menu **Fichier → Ouvrir un dossier…** et choisissez le dossier extrait. Dans la colonne de gauche de VS Code, vous devez voir directement les dossiers **`api`** et **`web`**. Si vous voyez à la place un autre dossier `ProjetCollection`, ouvrez plutôt celui-là.
3. Si VS Code demande « Faites-vous confiance aux auteurs ? », cliquez sur **Oui, je fais confiance aux auteurs**.

**Réglage à faire une seule fois** (il évite un blocage fréquent) :

1. Appuyez sur `Ctrl+Maj+P`, tapez `Terminal: Select Default Profile` et appuyez sur Entrée.
2. Choisissez **Command Prompt**.
3. Si un terminal est déjà ouvert en bas, fermez-le avec l'icône de **corbeille**.

## Étape 3 : créer la base de données

Cette étape se fait dans un programme à part, installé avec PostgreSQL.

1. Touche Windows, tapez **SQL Shell**, ouvrez **SQL Shell (psql)**.
2. La fenêtre pose quatre questions (Server, Database, Port, Username) : appuyez sur **Entrée** quatre fois.
3. Elle demande le mot de passe de l'étape 1 : tapez-le, puis Entrée. Rien ne s'affiche pendant la frappe, c'est normal.
4. Quand vous voyez `postgres=#`, copiez ces 3 lignes, faites un **clic droit** dans la fenêtre pour coller, puis Entrée :

```
CREATE USER ma_collection_user WITH PASSWORD 'collection2026';
CREATE DATABASE ma_collection OWNER ma_collection_user;
\q
```

Vous devez voir `CREATE ROLE` puis `CREATE DATABASE`. La fenêtre se ferme toute seule.

## Étape 4 : lancer l'API (terminal n°1)

1. Dans VS Code, colonne de gauche : **clic droit sur le dossier `api`** → **Ouvrir dans le terminal intégré**. Un terminal s'ouvre en bas, et son invite se termine par `\api>`.
2. Copiez-collez ces deux commandes, **une par une** (la deuxième dure 1 à 3 minutes) :

```
py -m venv .venv
```
```
.\.venv\Scripts\python -m pip install -r requirements.txt
```

Si Windows répond que `py` n'est pas reconnu, remplacez `py` par `python`. Si VS Code propose d'utiliser le nouvel environnement, cliquez sur **Oui**.

3. Générez une clé secrète pour le site :

```
.\.venv\Scripts\python -c "import secrets; print(secrets.token_hex(32))"
```

Une longue suite de caractères s'affiche. **Sélectionnez-la avec la souris** (maintenez le clic et glissez) puis copiez-la avec `Ctrl+C`.

4. Créez le fichier de configuration : **clic droit sur le dossier `api`** (colonne de gauche) → **Nouveau fichier** → tapez exactement `.env` → Entrée. Le fichier s'ouvre : collez-y ce texte, puis remplacez `COLLEZ_ICI_LA_CLE` par la clé copiée à l'étape précédente (`Ctrl+V`) :

```
DATABASE_URL=postgresql+asyncpg://ma_collection_user:collection2026@localhost:5432/ma_collection
JWT_SECRET_KEY=COLLEZ_ICI_LA_CLE
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

Enregistrez avec `Ctrl+S`.

5. Retournez dans le terminal (cliquez dedans) et remplissez la base avec les 40 recettes :

```
.\.venv\Scripts\python -m app.seed
```

Vous devez voir : `40 recette(s) ajoutée(s)`.

6. Démarrez l'API :

```
.\.venv\Scripts\python -m uvicorn app.main:app --reload
```

Vous devez voir `Application startup complete`. **Laissez ce terminal ouvert** et ne tapez plus rien dedans.

## Étape 5 : lancer le site (terminal n°2)

1. Colonne de gauche : **clic droit sur le dossier `web`** → **Ouvrir dans le terminal intégré**. Un deuxième terminal s'ouvre, et son invite se termine par `\web>`. Le premier terminal continue de tourner : vous pouvez passer de l'un à l'autre avec la liste qui apparaît à droite de la zone noire.
2. Copiez-collez, **une commande à la fois** (la première dure 1 à 2 minutes) :

```
npm install
```
```
npm run dev
```

Vous devez voir une ligne `Local: http://localhost:5173/`. **Laissez aussi ce terminal ouvert.**

## Étape 6 : utiliser le site

Ouvrez votre navigateur à l'adresse **http://localhost:5173**

1. Cliquez sur **Connexion**, puis sur **Pas encore de compte ? S'inscrire**, et créez votre compte.
2. Parcourez le catalogue (recherche, catégories), ouvrez une recette et ajoutez-la à votre collection.
3. Dans **Ma collection**, changez le statut, donnez une note ou supprimez. La page **Statistiques** résume le tout.

La documentation technique de l'API est visible sur http://localhost:8000/docs

## Arrêter, puis relancer un autre jour

- **Arrêter** : cliquez dans chaque terminal, appuyez sur `Ctrl+C`, puis fermez-le avec l'icône de corbeille.
- **Relancer** : l'installation n'est pas à refaire. PostgreSQL redémarre tout seul avec Windows. Faites un clic droit sur `api` → **Ouvrir dans le terminal intégré** et tapez `.\.venv\Scripts\python -m uvicorn app.main:app --reload`, puis un clic droit sur `web` → **Ouvrir dans le terminal intégré** et tapez `npm run dev`.

## Un problème ?

| Message ou symptôme | Que faire |
|---|---|
| `l'exécution de scripts est désactivée sur ce système` (en tapant `npm`) | Le terminal est en PowerShell. Fermez-le (corbeille) et refaites le **réglage de l'étape 2**. |
| `password authentication failed` | Le mot de passe du fichier `.env` n'est pas celui de l'étape 3. Ouvrez `api/.env` : la ligne `DATABASE_URL` doit contenir `collection2026`. |
| `connection refused` dans le terminal de l'API | PostgreSQL n'est pas démarré. Touche Windows, tapez `services`, ouvrez « Services », cherchez `postgresql-x64-…`, clic droit puis **Démarrer**. |
| `ModuleNotFoundError` | L'installation de l'étape 4 n'est pas allée jusqu'au bout. Relancez la commande `pip install -r requirements.txt` de l'étape 4 et attendez la fin. |
| Le site affiche « Impossible de charger le catalogue » | L'API n'est pas lancée (étape 4, point 6), ou la base n'a pas été remplie (point 5). |
| `py` ou `npm` « n'est pas reconnu » | Fermez VS Code complètement et rouvrez-le (les installations ne sont prises en compte qu'au redémarrage). Pour `py`, essayez `python`. |
| `address already in use` | Une ancienne fenêtre fait encore tourner le programme : fermez-la ou arrêtez-la avec `Ctrl+C`. |

## Linux / macOS (pour les habitués du terminal)

```bash
cd api
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
# créer api/.env comme à l'étape 4
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