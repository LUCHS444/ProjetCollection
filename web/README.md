# Ma Collection — Web (Frontend)

Interface React + TypeScript consommant l'API Ma Collection.

## Structure

src/
├── components/ # composants réutilisables (Navbar, ProtectedRoute)
├── contexts/ # AuthContext, CollectionContext
├── hooks/ # useLocalStorage, useDebounce
├── pages/ # ItemsPage, ItemDetailPage, LoginPage, CollectionPage, StatsPage
├── services/ # client HTTP unique (http.ts)
└── types/ # types du contrat d'API


## Lancement
```bash
npm install
npm run dev
```
Site disponible sur `http://localhost:5173`. L'API doit tourner sur `http://localhost:8000`.