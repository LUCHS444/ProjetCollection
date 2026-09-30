import { useEffect } from "react";
import { useCollection } from "../contexts/CollectionContext";

function StatsPage() {
  const { stats, erreur, fetchStats } = useCollection();

  useEffect(() => {
    fetchStats();
  }, [fetchStats]);

  if (erreur && !stats) {
    return <p className="erreur">{erreur}</p>;
  }

  if (!stats) {
    return <p>Chargement...</p>;
  }

  return (
    <div className="stats-page">
      <h1>Mes statistiques</h1>
      <p>Total d'éléments dans ma collection : {stats.total}</p>

      <h2>Répartition par statut</h2>
      {stats.total === 0 ? (
        <p>Aucune donnée pour le moment.</p>
      ) : (
        <ul>
          {Object.entries(stats.par_statut).map(([statut, count]) => (
            <li key={statut}>
              {statut} : {count}
            </li>
          ))}
        </ul>
      )}

      <h2>Note moyenne</h2>
      <p>{stats.note_moyenne !== null ? stats.note_moyenne.toFixed(2) : "Pas encore de note"}</p>
    </div>
  );
}

export default StatsPage;