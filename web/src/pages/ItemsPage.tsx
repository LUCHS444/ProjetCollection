import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { http } from "../services/http";
import useDebounce from "../hooks/useDebounce";
import type { ItemList } from "../types/api";

const CATEGORIES = ["Entrées", "Plats", "Desserts", "Boissons"];

function ItemsPage() {
  const [recherche, setRecherche] = useState<string>("");
  const [categorie, setCategorie] = useState<string>("");
  const [page, setPage] = useState<number>(1);
  const [data, setData] = useState<ItemList | null>(null);
  const [chargement, setChargement] = useState<boolean>(true);
  const [erreur, setErreur] = useState<string | null>(null);

  const rechercheDebounced = useDebounce(recherche, 400);
  const limit = 12;

  useEffect(() => {
    setPage(1);
  }, [rechercheDebounced, categorie]);

  useEffect(() => {
    let annule = false;

    async function fetchItems(): Promise<void> {
      setChargement(true);
      setErreur(null);
      try {
        const params = new URLSearchParams();
        if (rechercheDebounced.length >= 2) {
          params.set("q", rechercheDebounced);
        }
        if (categorie) {
          params.set("categorie", categorie);
        }
        params.set("page", String(page));
        params.set("limit", String(limit));

        const result = await http.get<ItemList>(`/items?${params.toString()}`);
        if (!annule) {
          setData(result);
        }
      } catch {
        if (!annule) {
          setErreur("Impossible de charger le catalogue.");
        }
      } finally {
        if (!annule) {
          setChargement(false);
        }
      }
    }

    fetchItems();

    return () => {
      annule = true;
    };
  }, [rechercheDebounced, categorie, page]);

  const totalPages = data ? Math.max(1, Math.ceil(data.total / limit)) : 1;

  return (
    <div className="items-page">
      <h1>Catalogue de recettes</h1>

      <div className="filtres">
        <input
          type="text"
          placeholder="Rechercher une recette..."
          value={recherche}
          onChange={(e) => setRecherche(e.target.value)}
        />

        <select value={categorie} onChange={(e) => setCategorie(e.target.value)}>
          <option value="">Toutes les catégories</option>
          {CATEGORIES.map((cat) => (
            <option key={cat} value={cat}>
              {cat}
            </option>
          ))}
        </select>
      </div>

      {chargement && <p>Chargement...</p>}
      {erreur && <p className="erreur">{erreur}</p>}
      {!chargement && !erreur && data && data.results.length === 0 && (
        <p>Aucune recette ne correspond à votre recherche.</p>
      )}

      {!chargement && !erreur && data && data.results.length > 0 && (
        <>
          <div className="items-grid">
            {data.results.map((item) => (
              <Link key={item.id} to={`/items/${item.id}`} className="item-card">
                <h3>{item.titre}</h3>
                <p>{item.categorie}</p>
                <p>{item.temps_preparation} min · {item.difficulte}</p>
              </Link>
            ))}
          </div>

          <div className="pagination">
            <button disabled={page <= 1} onClick={() => setPage((p) => p - 1)}>
              Précédent
            </button>
            <span>
              Page {page} / {totalPages}
            </span>
            <button disabled={page >= totalPages} onClick={() => setPage((p) => p + 1)}>
              Suivant
            </button>
          </div>
        </>
      )}
    </div>
  );
}

export default ItemsPage;