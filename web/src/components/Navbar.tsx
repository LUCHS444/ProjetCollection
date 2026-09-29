import { Link } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

function Navbar() {
  const { isAuthenticated, user, logout } = useAuth();

  return (
    <nav className="navbar">
      <Link to="/">Catalogue</Link>
      {isAuthenticated && <Link to="/collection">Ma collection</Link>}
      {isAuthenticated && <Link to="/stats">Statistiques</Link>}
      {isAuthenticated ? (
        <>
          <span>{user?.email}</span>
          <button onClick={logout}>Déconnexion</button>
        </>
      ) : (
        <Link to="/login">Connexion</Link>
      )}
    </nav>
  );
}

export default Navbar;