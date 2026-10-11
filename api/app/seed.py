import asyncio
import random
import re
import unicodedata

from sqlmodel import select
from urllib.parse import quote

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

IMAGES = {
    "Salade César": "https://imgs.search.brave.com/RgSR0wdUywu--ovN5-7y_Kk1G3pKY4tIQt36T-64qIQ/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9zdDIu/ZGVwb3NpdHBob3Rv/cy5jb20vMjcxNjQz/MS82ODU4L2kvNDUw/L2RlcG9zaXRwaG90/b3NfNjg1ODkxOTkt/c3RvY2stcGhvdG8t/Y2Flc2FyLXNhbGFk/LXdpdGgtY3JvdXRv/bnMtY2hlcnJ5Lmpw/Zw",
    "Velouté de potiron": "https://imgs.search.brave.com/EvenhaJAPtb803fpCRy3td388QDz9fCR4igr1owmhgw/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tb25t/ZW51LmZyL3Bob3Rv/cy80OTE1MjEuanBn",
    "Bruschetta tomate basilic": "https://imgs.search.brave.com/ACMnf6xE0aE48Qfk8zXzbglbmIA19GnjgQt3PPKva-c/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9taXRv/bm5lci5mci93cC1j/b250ZW50L3VwbG9h/ZHMvMjAyNS8xMi9S/ZWNldHRlLXNpbXBs/ZS1ldC1yYXBpZGUt/ZGUtYnJ1c2NoZXR0/YXMtdG9tYXRlcy1i/YXNpbGljLXBvdXIt/dW4tYXBlcml0aWYt/Z291cm1hbmQtNzY4/eDQxOS5qcGc",
    "Carpaccio de bœuf": "https://imgs.search.brave.com/lOQwJs2fBvwIHNJ9mOo1IFCNuY_cBRql5oAFah3rK6g/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9pbWct/My5qb3VybmFsZGVz/ZmVtbWVzLmZyLzZ5/dkM4QTFkWDBzUmZo/Z1ZMUWF0Y05rSDMy/VT0vNzUweDUwMC8y/YTYwZjhmMmI4ZjI0/ZWNkODFhMmQyMzk5/ODFkOTU3My9jY21j/bXMtamRmLzQwMDg5/NzAxLmpwZw",
    "Tarte fine aux légumes": "https://imgs.search.brave.com/F_MrJAl87wRPGbqA6mGxIC1PbP1WLshiHWNJ4NfIhjs/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9sZXNw/YXBpbGxlc2Rla2Fy/ZW4uY29tL3dwLWNv/bnRlbnQvdXBsb2Fk/cy8yMDI1LzA0L3dw/XzdjNzIxNF90YXJ0/ZS1maW5lLWF1eC1s/ZWd1bWVzLWR1LXNv/bGVpbC5KUEc",
    "Soupe à l'oignon gratinée": "https://imgs.search.brave.com/XeA8m4N8yDJHMeSdg9XQc4nDVAKA4eOGER2Lriz3LFE/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9jaGVm/Y3Vpc3RvLmNvbS9m/aWxlcy8yMDA4LzEx/L3NvdXBlLXBvaWdu/b24uanBn",
    "Œufs mimosa": "https://imgs.search.brave.com/Nw6zeMQhrAI4w8kRwB5I1dLzbI1IZyPqcyzNgDkaIi8/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9ibG9n/LnBvdXJkZWJvbi5j/b20vd3AtY29udGVu/dC91cGxvYWRzLzIw/MjQvMDMvY291di1t/aW1vc2EtNzUweDM3/NS5qcGc",
    "Houmous maison": "https://imgs.search.brave.com/osE0i_MoCxyKT4Fe38hXBo78n0EHSYNPtRimR1d1A3M/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly93d3cu/bGFjdWlzaW5lZGF1/cmVsaWUuY29tL3dw/LWNvbnRlbnQvdXBs/b2Fkcy8yMDIxLzA0/L0lNR183NzEzLTEy/NjB4ODQwLmpwZw",
    "Tartare de saumon": "https://imgs.search.brave.com/d26YIkIJxne5sKuVyLd2NyLdKnlc9QVPk8NphmG25o4/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly93d3cu/bGF5bGl0YS5jb20v/cmVjZXR0ZXMvd3At/Y29udGVudC91cGxv/YWRzLzIwMTkvMDQv/VGFydGFyZS1kZS1z/YXVtb24tYS1sYS1m/cmFuY2Fpc2UuanBn",
    "Terrine de campagne": "https://imgs.search.brave.com/13a68PngYDT3ToS_ib1pEkWs-gHxVVhIOF0XnzKPojI/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9jZG4u/bGFjdWlzaW5lZGFu/bmllLmNvbS9pbWFn/ZXMvNDQ5LmpwZw",
    "Bœuf bourguignon": "https://imgs.search.brave.com/S9HvOMN0yRADSQqOjp7_VRyJg_HUx_FX069pM46zoI0/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly90My5m/dGNkbi5uZXQvanBn/LzE1LzU3Lzc5Lzcy/LzM2MF9GXzE1NTc3/OTcyMTlfNHNlZzRL/WmlXb2gxZk5Zekcw/bzRYZExxZVZ4bGR4/dk0uanBn",
    "Poulet rôti aux herbes": "https://imgs.search.brave.com/BIAGk597O6lUHReDECx64N9M7cU95rHFT2ScKh75qKI/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly93d3cu/cGFwaWxsZXNldHB1/cGlsbGVzLmZyL3dw/LWNvbnRlbnQvdXBs/b2Fkcy8yMDIwLzA1/L1BvdWxldC1yJUMz/JUI0dGktYXV4LWhl/cmJlcy1Db3B5cmln/aHQtQ29jaG9uLXZv/bGFudC5qcGc",
    "Ratatouille": "https://imgs.search.brave.com/wl7DIQ4ubno3HAYUbysLS10AoVuE6awJFpPiHNxP9ik/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly90My5m/dGNkbi5uZXQvanBn/LzIwLzY3LzQwLzgy/LzM2MF9GXzIwNjc0/MDgyMjJfZU9IajhD/QVp6Sk12MVRXMzBX/am9jcTM3eGY0a3ZL/VHYuanBn",
    "Risotto aux champignons": "https://imgs.search.brave.com/6XopWhXfxUQxKCGqGunh2IPEG2O6sKWynaeJ8HWRq5I/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9zdGF0/aWM5LmRlcG9zaXRw/aG90b3MuY29tLzEw/NjY5NjEvMTE4MC9p/LzQ1MC9kZXBvc2l0/cGhvdG9zXzExODA0/OTI5LXN0b2NrLXBo/b3RvLW11c2hyb29t/LXJpc290dG8uanBn",
    "Curry de légumes": "https://imgs.search.brave.com/r4EOVEn9P1yR-np2qyfk-TKeMT-DRCbaQyu69O4ntTs/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly93d3cu/bmVzdGxlZ29vZG5l/cy5jb20vZnIvc2l0/ZXMvZGVmYXVsdC9m/aWxlcy9zdHlsZXMv/MV8xXzc2OHB4X3dp/ZHRoL3B1YmxpYy9z/cmhfcmVjaXBlcy8y/YWZlNGEzM2U3N2U4/N2Q5MDkyNjFkNGE2/NjRkYTQxMi5qcGVn/LndlYnA_aXRvaz1l/anM2U1l3Xw",
    "Lasagnes maison": "https://imgs.search.brave.com/nQSBx8Rp4ExR2R5Zdjr0VCrTpuhuSC6G3yz8C3NRtJI/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5pc3RvY2twaG90/by5jb20vaWQvNDgw/NTQxMjc4L2ZyL3Bo/b3RvL2xhc2FnbmVz/LWl0YWxpZW5uZXMt/ZXQtYmFzaWxpYy1m/cmFpcy1zdXItdW5l/LXBsYXRlLWhvcml6/b250YWxlcy5qcGc_/cz02MTJ4NjEyJnc9/MCZrPTIwJmM9cGJM/bktBTEdlVTZtdWZ6/Vzk1cXFjMHFwYjFI/TTNxT1BOd3VpMEJV/UTQ0TT0",
    "Saumon en papillote": "https://imgs.search.brave.com/DME4vA4ztCJO5HowcVWc27B-Z6xfip94CnYnu-mcJAA/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9lbWls/aWVyYW1lbmVzYWZy/YWlzZS5mci93cC1j/b250ZW50L3VwbG9h/ZHMvMjAxNC8wOS9w/YXBpbGxvdHRlLXNh/dW1vbi5qcGc",
    "Couscous royal": "https://imgs.search.brave.com/FOjwVuTO1glJUsbonPCezkm9RrLiLzAeVvkYEsckZyY/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5pc3RvY2twaG90/by5jb20vaWQvMTI5/NzI2NzYwNC9mci9w/aG90by9jb3Vjb3Vz/LXJveWFsLmpwZz9z/PTYxMng2MTImdz0w/Jms9MjAmYz1PU2Jy/T2swaGpGMzlLVzl6/RXJrYldKSlFXVnNx/OGh2NEUwcEVOMXR0/V28wPQ",
    "Blanquette de veau": "https://imgs.search.brave.com/zaeTCdnYKNfTzTR5ifl0oGJQUyOPVp5bI29csW0-lF4/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS1jZG4udHJpcGFk/dmlzb3IuY29tL21l/ZGlhL3Bob3RvLW8v/MTgvMWEvMmQvNWYv/YmxhbnF1ZXR0ZS1k/ZS12ZWF1LmpwZw",
    "Chili con carne": "https://imgs.search.brave.com/Xjq8whayPto5K1tMiObkWlTPjfivwfUoqHufOUe3nxA/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly90aHVt/YnMuZHJlYW1zdGlt/ZS5jb20vYi9jaGls/aS1jb24tY2FybmUt/Ym93bC13b29kZW4t/dGFibGUtYWktZ2Vu/ZXJhdGVkLTQyNzQ4/ODcyNy5qcGc",
    "Tartiflette": "https://imgs.search.brave.com/QyRS2VQMemOhxSn1vTi55P7hVjexSXk3QTvZHnKkk9o/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly90cnVj/bWFuaWEub3Vlc3Qt/ZnJhbmNlLmZyL3dw/LWNvbnRlbnQvdXBs/b2Fkcy8yMDI0LzEx/L3RhcnRpZmxldHRl/LmpwZw",
    "Pad thaï": "https://imgs.search.brave.com/lNmAxnWTDw_GYyESGSEFmnAC6ygSru5ktcnEjdVWflI/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly93d3cu/ZXZhc2lvbnNnb3Vy/bWFuZGVzLmNvbS93/cC1jb250ZW50L3Vw/bG9hZHMvY3Vpc2lu/ZV9kdV9tb25kZS9z/YXZldXJzX2FpbGxl/dXJzL3BhZF90aGFp/L3BhZF90aGFpX3Jl/Y2V0dGUuanBn",
    "Poke bowl saumon": "https://imgs.search.brave.com/Lgrhal3_bHqosdhHu_7Z8tfH_6nBoa4Ie6vD9oqWj2k/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9pbWct/My5qb3VybmFsZGVz/ZmVtbWVzLmZyL0dw/VDgxOUJqR3ZwVl9G/TUR1ZGk4V0V4NUlE/az0vNzUweDUwMC9k/Y2ZkMGI2YjZkMDc0/MGMzYmM4MWQ5MDY4/Mzk4NTM4MC9jY21j/bXMtamRmLzQwMDg4/MTkzLmpwZw",
    "Quiche lorraine": "https://imgs.search.brave.com/0eViJLXNISJrLxAUJ8O7NPlPt3XRSDDDVtpedrVOrrA/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly93d3cu/Ymllbm1hbmdlci5j/b20vdGlueU1jZURh/dGEvaW1hZ2VzL2Nv/bnRlbnRzLzU1NC9j/b250ZW50X2xnLmpw/Zw",
    "Paella": "https://imgs.search.brave.com/ioq_t9qRUf3KPHZjLo3C0pgUT8hh4BLnxJVxsoGncXY/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9pbWFn/ZXMucGV4ZWxzLmNv/bS9waG90b3MvMTY3/NDM0ODYvcGV4ZWxz/LXBob3RvLTE2NzQz/NDg2L2ZyZWUtcGhv/dG8tb2Ytbm91cnJp/dHVyZS1hbGltZW50/cy1yZXN0YXVyYW50/LXJlcGFzLmpwZWc_/Y3M9dGlueXNyZ2Im/ZHByPTEmdz01MDA",
    "Tarte au citron meringuée": "https://imgs.search.brave.com/aODE25kOfjopF5wGC_uX66prmhkIegcwWFn1nRizF5k/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9pbWct/My5qb3VybmFsZGVz/ZmVtbWVzLmZyL09p/RWRSYWpVdF9qTG5P/bEh5TGlQeXBNNzBR/TT0vNzUweDUwMC82/MDIwNTgxMzkxZDk0/NjdkOGNiNjgyNzhm/YTQ4OWVkZC9jY21j/bXMtamRmLzM5OTE2/NjE0LmpwZw",
    "Fondant au chocolat": "https://imgs.search.brave.com/VDTsvHwYOQ5lMf3c7ON1JfT0eHNhpPGjCoqVGvSgob8/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9zdGF0/aWMudmVjdGVlenku/Y29tL3RpL3Bob3Rv/cy1ncmF0dWl0ZS90/Mi81NjcxODAwOS1m/ZXJtZXItdnVlLWRl/LXJpY2hlcy1jaG9j/b2xhdC1mb25kYW50/LWJydWluZS1hdmVj/LWNob2NvbGF0LXNh/dWNlLXN1ci1hc3Np/ZXR0ZS1waG90by5q/cGc",
    "Crème brûlée": "https://imgs.search.brave.com/VDTXzLcFLynMOAexIVF_KRZxMIa7k2wRroxIUuvC8XU/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly90My5m/dGNkbi5uZXQvanBn/LzIwLzUzLzI2LzY4/LzM2MF9GXzIwNTMy/NjY4MDdfRWNNYjJk/M1dRVjFkT21JQVhl/WmVrQ0htN3NjNm1B/eE0uanBn",
    "Tiramisu": "https://imgs.search.brave.com/bN7GVx3Nbxo8F3bd0w0KSRJra5oFlGJaeXdQBAfUAas/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9zdDIu/ZGVwb3NpdHBob3Rv/cy5jb20vMTAwMDMz/Ni8xMDA2OC9pLzQ1/MC9kZXBvc2l0cGhv/dG9zXzEwMDY4NDk1/OC1zdG9jay1waG90/by10aXJhbWlzdS1j/YWtlLW9uLXBsYXRl/LmpwZw",
    "Mousse au chocolat": "https://imgs.search.brave.com/0giDl9RmHD58rZTrnltLLAgPPZERrCncMcZqxZqjPtU/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9zdGF0/aWMudmVjdGVlenku/Y29tL3RpL3Bob3Rv/cy1ncmF0dWl0ZS90/Mi80OTg3MzU3MC1y/ZXN0YXVyYW50LWNo/b2NvbGF0LW1vdXNz/ZS1kZXNzZXJ0LXBo/b3RvLmpwZWc",
    "Crumble aux pommes": "https://imgs.search.brave.com/0wdP2j-D1ktYW2cy0eupTcFQWUj_Gf6Wk801acBiPjQ/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5pc3RvY2twaG90/by5jb20vaWQvMTc1/MjI3NTk2L2ZyL3Bo/b3RvL2FwcGxlLXNv/eWV1eC5qcGc_cz02/MTJ4NjEyJnc9MCZr/PTIwJmM9M0MtTXQ2/NlJ2cHBBdjZkWFAw/c1JQTG05a2J6R0pT/SU14ZnlIbmxYLUtD/Yz0",
    "Panna cotta aux fruits rouges": "https://imgs.search.brave.com/GuT2PSCd84EPo4CfyJNwmm3NMdGeigcDeHhoUHE4IMw/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly93d3cu/bGVzMm1hcm1vdHRl/cy5jb20vY2RuL3No/b3AvZmlsZXMvdi1y/ZWNldHRlLXBhbm5h/Y290dGEtZnJ1aXRz/LXJvdWdlcy5qcGc_/dj0xNzg3MTMxMDc3/JndpZHRoPTM4NDA",
    "Paris-Brest": "https://imgs.search.brave.com/uqnrbyLyo4Y2Qm2osXEM_5koTzWRputsRf8_JcheTUc/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9maWxl/cy5tZWlsbGV1cmR1/Y2hlZi5jb20vbWRj/L3Bob3RvL3JlY2V0/dGUvcGFyaXMtYnJl/c3QvcGFyaXMtYnJl/c3QtNjQwLmpwZw",
    "Cheesecake New-York": "https://imgs.search.brave.com/wn2eKCI9fwHi08TS9uTfJQu4_LtAOyFWpkRvVQJamBU/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9pMC53/cC5jb20vd3d3LnJl/Y2V0dGVzZGVjdWlz/aW5lZHVtb25kZS5j/b20vd3AtY29udGVu/dC91cGxvYWRzLzIw/MTYvMDEvTlktQ2hl/ZXNlY2FrZS1wYXIt/RmFubnkuanBnP3Jl/c2l6ZT01NzAsNDEz",
    "Île flottante": "https://imgs.search.brave.com/kvBQEOY0_OvliLcRgwCD4Tznn99sgGGAkTDceUGUKs8/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly93d3cu/anVsaWVhbmRyaWV1/LmNvbS9tZWRpYS9j/YWNoZS93ZWJfcmVj/aXBlX2RldGFpbC91/cGxvYWRzL3JlY2V0/dGVzL2Rlc3NlcnQv/aWxlLWZsb3R0YW50/ZS5qcGc",
    "Mojito sans alcool": "https://imgs.search.brave.com/bZymxZ_85YhKQ2r4h5ajNxzMRLbv2romEsfqoSRArxY/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9pbWct/My5qb3VybmFsZGVz/ZmVtbWVzLmZyL2ND/ZDNWN25XaTFqZHB2/aVJGU3h3QVptd2JM/ST0vNzUweDUwMC8y/NDcxNWZhYmRlMmQ0/YTZmYjI1NDBkZTlm/NmU1MmQ5MS9jY21j/bXMtamRmLzM5NzA1/NzU1LmpwZw",
    "Smoothie mangue passion": "https://imgs.search.brave.com/tqmFuvpP92R8ZTXnySq2qG12d8CtjsFwzSKNsK2OFU4/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9pbWcu/Y3Vpc2luZWF6LmNv/bS82NjB4NDk1LzIw/MTMvMTIvMjAvaTkx/MDkwLXNtb290aGll/LW1hbmd1ZS1wYXNz/aW9uLmpwZWc",
    "Chocolat chaud maison": "https://imgs.search.brave.com/qhmbVhjaLP11bjQfyast8Z1SrY-iRvmQnPslqma3ZEg/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly93d3cu/cmVjZXR0ZXMtY2hv/Y29sYXRzLmNvbS9o/YnN0cmcvMjAyNS8x/Mi9DaG9jb2xhdC1j/aGF1ZC1tYWlzb24u/d2VicA",
    "Thé glacé pêche": "https://imgs.search.brave.com/pptn3b2n_l_hpoqig8fovU11T6KrCYrrMiIEGSg1Edg/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5pc3RvY2twaG90/by5jb20vaWQvNDgz/NzU5ODY2L2ZyL3Bo/b3RvL3RoJUMzJUE5/LWdsYWMlQzMlQTkt/YXZlYy1kZXMtbSVD/MyVCQnJlcy1wZWFj/aGVzLXN1ci1mb25k/LXJ1c3RpcXVlLmpw/Zz9zPTYxMng2MTIm/dz0wJms9MjAmYz1V/dnI5VjIwcVU1ZFph/Wml6clBmWFJlbFlD/Qi1CcWZRTWJlRnVC/RjRPVFVvPQ",
    "Limonade maison": "https://imgs.search.brave.com/hnaXC6nj50h4iM4br20Askp83C6LOFTPkmei3x_H_ps/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly90b3Bh/c3NpZXR0ZS5jb20v/YXNzZXRzL2ltYWdl/cy8xNzQ5NjQ0NTI5/MTM3LXk1d2c5bGNu/LndlYnA",
}

def slugify(texte: str) -> str:
    """Convertit un titre en nom de fichier simple, sans accents ni espaces."""
    texte = unicodedata.normalize("NFKD", texte)
    texte = "".join(c for c in texte if not unicodedata.combining(c))
    texte = texte.lower()
    texte = re.sub(r"[^a-z0-9]+", "-", texte).strip("-")
    return texte


for r in RECETTES:
    image = IMAGES.get(r["titre"], "").strip()
    r["image_url"] = image or f"/images/recettes/{slugify(r['titre'])}.jpg"


async def seed():
    await init_db()
    async with async_session_maker() as session:
        result = await session.exec(select(Item))
        existants = {item.titre: item for item in result.all()}

        nouveaux = 0
        mis_a_jour = 0

        for r in RECETTES:
            if r["titre"] in existants:
                item = existants[r["titre"]]
                if item.image_url != r["image_url"]:
                    item.image_url = r["image_url"]
                    session.add(item)
                    mis_a_jour += 1
            else:
                session.add(Item(**r))
                nouveaux += 1

        await session.commit()
        print(f"{nouveaux} recette(s) ajoutée(s), {mis_a_jour} image(s) mise(s) à jour.")


if __name__ == "__main__":
    asyncio.run(seed())