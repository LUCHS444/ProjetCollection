import asyncio
import random

from sqlmodel import select

from app.db.session import async_session_maker, init_db
from app.models.item import Item

RECETTES = [
    # Entrées
    {"titre": "Salade César", "categorie": "Entrées", "description": "Salade croquante, poulet grillé, parmesan et sauce César maison.", "temps_preparation": 15, "difficulte": "facile", "type_plat": "entree"},
    {"titre": "Velouté de potiron", "categorie": "Entrées", "description": "Soupe onctueuse au potiron et à la crème fraîche.", "temps_preparation": 30, "difficulte": "facile", "type_plat": "entree"},
    {"titre": "Bruschetta tomate basilic", "categorie": "Entrées", "description": "Pain grillé garni de tomates fraîches, basilic et huile d'olive.", "temps_preparation": 10, "difficulte": "facile", "type_plat": "entree"},
    {"titre": "Carpaccio de bœuf", "categorie": "Entrées", "description": "Fines tranches de bœuf, copeaux de parmesan, roquette et citron.", "temps_preparation": 20, "difficulte": "moyen", "type_plat": "entree"},
    {"titre": "Tarte fine aux légumes", "categorie": "Entrées", "description": "Pâte feuilletée garnie de légumes de saison rôtis.", "temps_preparation": 35, "difficulte": "moyen", "type_plat": "entree"},
    {"titre": "Soupe à l'oignon gratinée", "categorie": "Entrées", "description": "Soupe traditionnelle française, gratinée au fromage.", "temps_preparation": 45, "difficulte": "moyen", "type_plat": "entree"},
    {"titre": "Œufs mimosa", "categorie": "Entrées", "description": "Œufs durs garnis d'une farce mayonnaise et jaune d'œuf.", "temps_preparation": 20, "difficulte": "facile", "type_plat": "entree"},
    {"titre": "Houmous maison", "categorie": "Entrées", "description": "Purée de pois chiches, tahini, citron et ail.", "temps_preparation": 15, "difficulte": "facile", "type_plat": "entree"},
    {"titre": "Tartare de saumon", "categorie": "Entrées", "description": "Saumon frais coupé au couteau, avocat, citron vert et aneth.", "temps_preparation": 20, "difficulte": "moyen", "type_plat": "entree"},
    {"titre": "Terrine de campagne", "categorie": "Entrées", "description": "Terrine de porc traditionnelle, servie avec des cornichons.", "temps_preparation": 90, "difficulte": "difficile", "type_plat": "entree"},

    # Plats
    {"titre": "Bœuf bourguignon", "categorie": "Plats", "description": "Ragoût de bœuf mijoté au vin rouge avec carottes et champignons.", "temps_preparation": 180, "difficulte": "difficile", "type_plat": "plat"},
    {"titre": "Poulet rôti aux herbes", "categorie": "Plats", "description": "Poulet fermier rôti au four, farci d'herbes fraîches.", "temps_preparation": 90, "difficulte": "moyen", "type_plat": "plat"},
    {"titre": "Ratatouille", "categorie": "Plats", "description": "Mijoté de légumes du sud, courgettes, aubergines, poivrons.", "temps_preparation": 60, "difficulte": "moyen", "type_plat": "plat"},
    {"titre": "Risotto aux champignons", "categorie": "Plats", "description": "Riz arborio crémeux, champignons de Paris et parmesan.", "temps_preparation": 40, "difficulte": "moyen", "type_plat": "plat"},
    {"titre": "Curry de légumes", "categorie": "Plats", "description": "Curry doux au lait de coco, légumes variés et riz basmati.", "temps_preparation": 45, "difficulte": "facile", "type_plat": "plat"},
    {"titre": "Lasagnes maison", "categorie": "Plats", "description": "Lasagnes à la bolognaise et béchamel, gratinées au four.", "temps_preparation": 90, "difficulte": "moyen", "type_plat": "plat"},
    {"titre": "Saumon en papillote", "categorie": "Plats", "description": "Pavé de saumon cuit vapeur avec légumes et citron.", "temps_preparation": 30, "difficulte": "facile", "type_plat": "plat"},
    {"titre": "Couscous royal", "categorie": "Plats", "description": "Semoule, merguez, agneau, poulet et légumes mijotés.", "temps_preparation": 150, "difficulte": "difficile", "type_plat": "plat"},
    {"titre": "Blanquette de veau", "categorie": "Plats", "description": "Veau mijoté dans une sauce crémeuse aux champignons.", "temps_preparation": 120, "difficulte": "difficile", "type_plat": "plat"},
    {"titre": "Chili con carne", "categorie": "Plats", "description": "Viande hachée mijotée avec haricots rouges et épices.", "temps_preparation": 60, "difficulte": "facile", "type_plat": "plat"},
    {"titre": "Tartiflette", "categorie": "Plats", "description": "Gratin savoyard aux pommes de terre, reblochon et lardons.", "temps_preparation": 60, "difficulte": "moyen", "type_plat": "plat"},
    {"titre": "Pad thaï", "categorie": "Plats", "description": "Nouilles de riz sautées, crevettes, cacahuètes et sauce tamarin.", "temps_preparation": 30, "difficulte": "moyen", "type_plat": "plat"},
    {"titre": "Poke bowl saumon", "categorie": "Plats", "description": "Riz, saumon cru mariné, avocat, edamame et sauce soja.", "temps_preparation": 25, "difficulte": "facile", "type_plat": "plat"},
    {"titre": "Quiche lorraine", "categorie": "Plats", "description": "Tarte salée aux lardons, œufs et crème fraîche.", "temps_preparation": 50, "difficulte": "facile", "type_plat": "plat"},
    {"titre": "Paella", "categorie": "Plats", "description": "Riz espagnol au safran, fruits de mer et poulet.", "temps_preparation": 75, "difficulte": "difficile", "type_plat": "plat"},

    # Desserts
    {"titre": "Tarte au citron meringuée", "categorie": "Desserts", "description": "Pâte sablée, crème citron et meringue italienne.", "temps_preparation": 60, "difficulte": "difficile", "type_plat": "dessert"},
    {"titre": "Fondant au chocolat", "categorie": "Desserts", "description": "Gâteau au chocolat coulant, cœur fondant.", "temps_preparation": 30, "difficulte": "facile", "type_plat": "dessert"},
    {"titre": "Crème brûlée", "categorie": "Desserts", "description": "Crème vanille onctueuse, caramélisée au chalumeau.", "temps_preparation": 45, "difficulte": "moyen", "type_plat": "dessert"},
    {"titre": "Tiramisu", "categorie": "Desserts", "description": "Dessert italien au café, mascarpone et biscuits cuillère.", "temps_preparation": 30, "difficulte": "facile", "type_plat": "dessert"},
    {"titre": "Mousse au chocolat", "categorie": "Desserts", "description": "Mousse aérienne au chocolat noir, sans crème.", "temps_preparation": 20, "difficulte": "facile", "type_plat": "dessert"},
    {"titre": "Crumble aux pommes", "categorie": "Desserts", "description": "Pommes fondantes sous une croûte croustillante à l'avoine.", "temps_preparation": 45, "difficulte": "facile", "type_plat": "dessert"},
    {"titre": "Panna cotta aux fruits rouges", "categorie": "Desserts", "description": "Crème italienne à la vanille, coulis de fruits rouges.", "temps_preparation": 25, "difficulte": "facile", "type_plat": "dessert"},
    {"titre": "Paris-Brest", "categorie": "Desserts", "description": "Pâte à choux garnie de crème pralinée.", "temps_preparation": 90, "difficulte": "difficile", "type_plat": "dessert"},
    {"titre": "Cheesecake New-York", "categorie": "Desserts", "description": "Gâteau au fromage frais sur base de biscuits.", "temps_preparation": 75, "difficulte": "moyen", "type_plat": "dessert"},
    {"titre": "Île flottante", "categorie": "Desserts", "description": "Blancs en neige pochés sur une crème anglaise.", "temps_preparation": 40, "difficulte": "moyen", "type_plat": "dessert"},

    # Boissons
    {"titre": "Mojito sans alcool", "categorie": "Boissons", "description": "Citron vert, menthe fraîche, sucre de canne et eau gazeuse.", "temps_preparation": 10, "difficulte": "facile", "type_plat": "boisson"},
    {"titre": "Smoothie mangue passion", "categorie": "Boissons", "description": "Mangue, fruit de la passion et lait de coco mixés.", "temps_preparation": 5, "difficulte": "facile", "type_plat": "boisson"},
    {"titre": "Chocolat chaud maison", "categorie": "Boissons", "description": "Lait chaud, chocolat noir fondu et une pointe de vanille.", "temps_preparation": 10, "difficulte": "facile", "type_plat": "boisson"},
    {"titre": "Thé glacé pêche", "categorie": "Boissons", "description": "Thé noir infusé, sirop de pêche et glaçons.", "temps_preparation": 15, "difficulte": "facile", "type_plat": "boisson"},
    {"titre": "Limonade maison", "categorie": "Boissons", "description": "Citrons pressés, sucre et eau pétillante.", "temps_preparation": 10, "difficulte": "facile", "type_plat": "boisson"},
]


async def seed():
    await init_db()
    async with async_session_maker() as session:
        result = await session.exec(select(Item.titre))
        existing_titles = set(result.all())

        nouveaux = [Item(**r) for r in RECETTES if r["titre"] not in existing_titles]

        if not nouveaux:
            print("Aucune nouvelle recette à ajouter, la base est déjà peuplée.")
            return

        session.add_all(nouveaux)
        await session.commit()
        print(f"{len(nouveaux)} recette(s) ajoutée(s). Total dans le fichier : {len(RECETTES)}.")


if __name__ == "__main__":
    asyncio.run(seed())