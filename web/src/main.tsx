import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./index.css";
import { AuthProvider } from "./contexts/AuthContext";
import { CollectionProvider } from "./contexts/CollectionContext";
import ProtectedRoute from "./components/ProtectedRoute";
import LoginPage from "./pages/LoginPage";
import ItemsPage from "./pages/ItemsPage";
import ItemDetailPage from "./pages/ItemDetailPage";
import CollectionPage from "./pages/CollectionPage";
import StatsPage from "./pages/StatsPage";
import Navbar from "./components/Navbar";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <CollectionProvider>
          <Navbar />
          <Routes>
            <Route element={<ProtectedRoute />}>
              <Route path="/collection" element={<CollectionPage />} />
              <Route path="/stats" element={<StatsPage />} />
            </Route>
            <Route path="/" element={<ItemsPage />} />
            <Route path="/items/:id" element={<ItemDetailPage />} />
            <Route path="/login" element={<LoginPage />} />
          </Routes>
        </CollectionProvider>
      </AuthProvider>
    </BrowserRouter>
  </StrictMode>
);