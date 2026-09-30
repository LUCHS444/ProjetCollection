import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { http } from "../services/http";
import { useAuth } from "../contexts/AuthContext";
import { useCollection } from "../contexts/CollectionContext";
import type { Item, Statut } from "../types/api";

function ItemDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [item, setItem] = useState<Item | null>(null);
  const [chargement, setChargement] = useState<boolean>(true);
  const [erreur, setErreur] = useState<string | null>(null);
  const [messageAjout, setMessageAjout] = useState<string | null>(null);

  const { isAuthenticated } = useAuth();
  const { addEntry } = useCollection();

  useEffect(() => {
    if (!id) return;

    let annule = false;

    async function fetchItem(): Promise<void> {
      setChargement(true);
      setErreur(null);
      try {
        const result = await http.get<Item>(`/items/${id}`);
        if (!annule) {
          setItem(result);
        }
      } catch {
        if (!annule) {
          setErreur("Cette recette est introuvable.");
        }
      } finally {
        if (!annule) {
          setChargement(false);
        }
      }
    }

    fetchItem();

    return () => {
      annule = true;
    };
  }, [id]);

  async function handleAjouter(statut: Statut): Promise<void> {
    if (!item) return;
    setMessageAjout(null);
    try {
      await addEntry({ item_id: item.id, statut });
      setMessageAjout("Ajouté à votre collection !");
    } catch {
      setMessageAjout("Impossible d'ajouter cette recette (déjà présente ?).");
    }
  }

  if (chargement) {
    return <p>Chargement...</p>;
  }

  if (erreur || !item) {
    return <p className="erreur">{erreur ?? "Recette introuvable."}</p>;
  }

  return (
    <div className="item-detail-page">
      <Link to="/">← Retour au catalogue</Link>
      <h1>{item.titre}</h1>
      {item.image_url && (
        <img src={item.image_url} alt={item.titre} className="item-detail-image" />
      )}
      <p className="categorie">{item.categorie}</p>
      <p>{item.description}</p>
      <ul className="item-meta">
        <li>Temps de préparation : {item.temps_preparation} min</li>
        <li>Difficulté : {item.difficulte}</li>
        <li>Type de plat : {item.type_plat}</li>
      </ul>

      {isAuthenticated ? (
        <div className="actions-collection">
          <button onClick={() => handleAjouter("a_decouvrir")}>À découvrir</button>
          <button onClick={() => handleAjouter("en_cours")}>En cours</button>
          <button onClick={() => handleAjouter("termine")}>Terminé</button>
          {messageAjout && <p>{messageAjout}</p>}
        </div>
      ) : (
        <p>
          <Link to="/login">Connectez-vous</Link> pour ajouter cette recette à votre collection.
        </p>
      )}
    </div>
  );
}

export default ItemDetailPage;