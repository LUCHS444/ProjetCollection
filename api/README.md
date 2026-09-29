README backend (api/README.md)
markdown
# Ma Collection — API (Backend)

API REST FastAPI pour le catalogue de recettes et la gestion de collections personnelles.

## Structure

app/
├── core/ # configuration, sécurité (JWT, bcrypt)
├── db/ # connexion base de données
├── dependencies/ # dépendances FastAPI (auth)
├── models/ # modèles SQLModel (User, Item, Entry)
├── routers/ # routes (auth, items, collection)
├── schemas/ # schémas Pydantic (entrée/sortie API)
├── main.py # assemblage de l'application
└── seed.py # script de peuplement du catalogue


## Lancement
Voir le README à la racine du dépôt pour la procédure complète (PostgreSQL + venv + .env).

```bash
source .venv/bin/activate
python -m uvicorn app.main:app --reload
```

Documentation interactive : `http://localhost:8000/docs`