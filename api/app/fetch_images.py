import json
import os
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

from app.seed import RECETTES, slugify

# Requêtes en anglais : Pexels renvoie de bien meilleurs résultats
REQUETES = {
    "Salade César": "caesar salad",
    "Velouté de potiron": "pumpkin soup",
    "Bruschetta tomate basilic": "tomato basil bruschetta",
    "Carpaccio de bœuf": "beef carpaccio",
    "Tarte fine aux légumes": "vegetable tart",
    "Soupe à l'oignon gratinée": "french onion soup",
    "Œufs mimosa": "deviled eggs",
    "Houmous maison": "hummus",
    "Tartare de saumon": "salmon tartare",
    "Terrine de campagne": "country pate terrine",
    "Bœuf bourguignon": "beef bourguignon",
    "Poulet rôti aux herbes": "roast chicken herbs",
    "Ratatouille": "ratatouille",
    "Risotto aux champignons": "mushroom risotto",
    "Curry de légumes": "vegetable curry",
    "Lasagnes maison": "lasagna",
    "Saumon en papillote": "baked salmon vegetables",
    "Couscous royal": "couscous lamb merguez",
    "Blanquette de veau": "veal stew cream sauce",
    "Chili con carne": "chili con carne",
    "Tartiflette": "tartiflette",
    "Pad thaï": "pad thai",
    "Poke bowl saumon": "salmon poke bowl",
    "Quiche lorraine": "quiche lorraine",
    "Paella": "paella",
    "Tarte au citron meringuée": "lemon meringue pie",
    "Fondant au chocolat": "chocolate lava cake",
    "Crème brûlée": "creme brulee",
    "Tiramisu": "tiramisu",
    "Mousse au chocolat": "chocolate mousse",
    "Crumble aux pommes": "apple crumble",
    "Panna cotta aux fruits rouges": "panna cotta berries",
    "Paris-Brest": "paris brest pastry",
    "Cheesecake New-York": "new york cheesecake",
    "Île flottante": "floating island dessert",
    "Mojito sans alcool": "virgin mojito mint lime",
    "Smoothie mangue passion": "mango passion fruit smoothie",
    "Chocolat chaud maison": "hot chocolate",
    "Thé glacé pêche": "peach iced tea",
    "Limonade maison": "homemade lemonade",
}

DOSSIER = Path(__file__).resolve().parents[1] / "web" / "public" / "images" / "recettes"
EN_TETES = {"User-Agent": "Mozilla/5.0 (projet scolaire Ma Collection)"}


def chercher_photo(requete: str, cle: str) -> str | None:
    url = "https://api.pexels.com/v1/search?" + urllib.parse.urlencode(
        {"query": requete, "orientation": "landscape", "per_page": 1}
    )
    req = urllib.request.Request(url, headers={**EN_TETES, "Authorization": cle})
    with urllib.request.urlopen(req, timeout=20) as reponse:
        data = json.load(reponse)
    photos = data.get("photos", [])
    return photos[0]["src"]["large"] if photos else None


def telecharger(url: str, destination: Path) -> None:
    req = urllib.request.Request(url, headers=EN_TETES)
    with urllib.request.urlopen(req, timeout=30) as reponse:
        destination.write_bytes(reponse.read())


def main() -> None:
    cle = os.environ.get("PEXELS_API_KEY")
    if not cle:
        sys.exit("Variable PEXELS_API_KEY manquante (voir instructions).")

    DOSSIER.mkdir(parents=True, exist_ok=True)

    for r in RECETTES:
        titre = r["titre"]
        fichier = DOSSIER / f"{slugify(titre)}.jpg"
        if fichier.exists():
            print(f"= {titre} (déjà présent)")
            continue
        requete = REQUETES.get(titre, titre)
        try:
            url = chercher_photo(requete, cle)
            if url is None:
                print(f"! {titre} : aucune photo pour '{requete}'")
                continue
            telecharger(url, fichier)
            print(f"+ {titre}")
        except Exception as e:
            print(f"! {titre} : {e}")
        time.sleep(0.5)


if __name__ == "__main__":
    main()