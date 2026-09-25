// --- Authentification ---

export interface UserCreate {
  email: string;
  password: string;
}

export interface UserLogin {
  email: string;
  password: string;
}

export interface UserRead {
  id: number;
  email: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}

// --- Catalogue ---

export type Difficulte = "facile" | "moyen" | "difficile";
export type TypePlat = "entree" | "plat" | "dessert" | "boisson" | "autre";

export interface Item {
  id: number;
  titre: string;
  categorie: string;
  description: string;
  image_url: string | null;
  temps_preparation: number;
  difficulte: Difficulte;
  type_plat: TypePlat;
}

export interface ItemList {
  total: number;
  page: number;
  limit: number;
  results: Item[];
}

// --- Collection personnelle ---

export type Statut = "a_decouvrir" | "en_cours" | "termine";

export interface EntryCreate {
  item_id: number;
  statut: Statut;
  note?: number;
  commentaire?: string;
}

export interface EntryUpdate {
  statut?: Statut;
  note?: number;
  commentaire?: string;
}

export interface Entry {
  id: number;
  statut: Statut;
  note: number | null;
  commentaire: string | null;
  date_ajout: string;
  item: Item;
}

export interface Stats {
  total: number;
  par_statut: Record<string, number>;
  note_moyenne: number | null;
}

// --- Erreurs ---

export interface ApiErrorBody {
  erreur: {
    code: number;
    message: string;
  };
}