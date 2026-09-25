import { createContext, useContext, useState, useCallback, type ReactNode } from "react";
import { http } from "../services/http";
import type { Entry, EntryCreate, EntryUpdate, Stats } from "../types/api";

interface CollectionContextValue {
  entries: Entry[];
  stats: Stats | null;
  chargement: boolean;
  erreur: string | null;
  fetchCollection: () => Promise<void>;
  fetchStats: () => Promise<void>;
  addEntry: (data: EntryCreate) => Promise<void>;
  updateEntry: (id: number, data: EntryUpdate) => Promise<void>;
  deleteEntry: (id: number) => Promise<void>;
}

const CollectionContext = createContext<CollectionContextValue | undefined>(undefined);

export function CollectionProvider({ children }: { children: ReactNode }) {
  const [entries, setEntries] = useState<Entry[]>([]);
  const [stats, setStats] = useState<Stats | null>(null);
  const [chargement, setChargement] = useState<boolean>(false);
  const [erreur, setErreur] = useState<string | null>(null);

  const fetchCollection = useCallback(async (): Promise<void> => {
    setChargement(true);
    setErreur(null);
    try {
      const data = await http.get<Entry[]>("/me/collection");
      setEntries(data);
    } catch {
      setErreur("Impossible de charger votre collection.");
    } finally {
      setChargement(false);
    }
  }, []);

  const fetchStats = useCallback(async (): Promise<void> => {
    try {
      const data = await http.get<Stats>("/me/stats");
      setStats(data);
    } catch {
      setErreur("Impossible de charger les statistiques.");
    }
  }, []);

  async function addEntry(data: EntryCreate): Promise<void> {
    await http.post<Entry>("/me/collection", data);
    await fetchCollection();
    await fetchStats();
  }

  async function updateEntry(id: number, data: EntryUpdate): Promise<void> {
    await http.patch<Entry>(`/me/collection/${id}`, data);
    await fetchCollection();
    await fetchStats();
  }

  async function deleteEntry(id: number): Promise<void> {
    await http.delete<void>(`/me/collection/${id}`);
    await fetchCollection();
    await fetchStats();
  }

  const value: CollectionContextValue = {
    entries,
    stats,
    chargement,
    erreur,
    fetchCollection,
    fetchStats,
    addEntry,
    updateEntry,
    deleteEntry,
  };

  return <CollectionContext.Provider value={value}>{children}</CollectionContext.Provider>;
}

export function useCollection(): CollectionContextValue {
  const context = useContext(CollectionContext);
  if (context === undefined) {
    throw new Error("useCollection doit être utilisé à l'intérieur d'un CollectionProvider");
  }
  return context;
}