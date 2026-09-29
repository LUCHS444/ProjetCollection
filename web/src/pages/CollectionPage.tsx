import { useEffect, useState } from "react";
import { useCollection } from "../contexts/CollectionContext";
import type { Statut } from "../types/api";

const STATUTS: { value: Statut; label: string }[] = [
  { value: "a_decouvrir", label: "À découvrir" },
  { value: "en_cours", label: "En cours" },
  { value: "termine", label: "Terminé" },
];

function CollectionPage() {
  const { entries, chargement, erreur, fetchCollection, updateEntry, deleteEntry } = useCollection();
  const [filtreStatut, setFiltreStatut] = useState<string>("");

  useEffect(() => {
    fetchCollection();
  }, [fetchCollection]);

  const entriesFiltrees = filtreStatut
    ? entries.filter((e) => e.statut === filtreStatut)
    : entries;

  async function handleStatutChange(id: number, statut: Statut): Promise<void> {
    await updateEntry(id, { statut });
  }

  async function handleNoteChange(id: number, note: number): Promise<void> {
    await updateEntry(id, { note });
  }

  async function handleDelete(id: number): Promise<void> {
    await deleteEntry(id);
  }

  return (
    <div className="collection-page">
      <h1>Ma collection</h1>

      <select value={filtreStatut} onChange={(e) => setFiltreStatut(e.target.value)}>
        <option value="">Tous les statuts</option>
        {STATUTS.map((s) => (
          <option key={s.value} value={s.value}>
            {s.label}
          </option>
        ))}
      </select>

      {chargement && <p>Chargement...</p>}
      {erreur && <p className="erreur">{erreur}</p>}
      {!chargement && !erreur && entriesFiltrees.length === 0 && (
        <p>Votre collection est vide pour ce filtre.</p>
      )}

      {!chargement && !erreur && entriesFiltrees.length > 0 && (
        <ul className="collection-list">
          {entriesFiltrees.map((entry) => (
            <li key={entry.id} className="collection-item">
              <h3>{entry.item.titre}</h3>
              <p>{entry.item.categorie}</p>

              <label>
                Statut :
                <select
                  value={entry.statut}
                  onChange={(e) => handleStatutChange(entry.id, e.target.value as Statut)}
                >
                  {STATUTS.map((s) => (
                    <option key={s.value} value={s.value}>
                      {s.label}
                    </option>
                  ))}
                </select>
              </label>

              <label>
                Note :
                <select
                  value={entry.note ?? ""}
                  onChange={(e) =>
                    handleNoteChange(entry.id, Number(e.target.value))
                  }
                >
                  <option value="">—</option>
                  {[1, 2, 3, 4, 5].map((n) => (
                    <option key={n} value={n}>
                      {n}
                    </option>
                  ))}
                </select>
              </label>

              <button onClick={() => handleDelete(entry.id)}>Supprimer</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default CollectionPage;