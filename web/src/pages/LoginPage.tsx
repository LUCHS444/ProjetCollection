import { useState, type FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { ApiError } from "../services/http";

function LoginPage() {
  const [mode, setMode] = useState<"login" | "register">("login");
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [chargement, setChargement] = useState<boolean>(false);
  const [erreur, setErreur] = useState<string | null>(null);

  const { login, register } = useAuth();
  const navigate = useNavigate();

  async function handleSubmit(e: FormEvent<HTMLFormElement>): Promise<void> {
    e.preventDefault();
    setErreur(null);
    setChargement(true);

    try {
      if (mode === "login") {
        await login({ email, password });
      } else {
        await register({ email, password });
      }
      navigate("/collection");
    } catch (err) {
      if (err instanceof ApiError) {
        setErreur(err.message);
      } else {
        setErreur("Une erreur inattendue est survenue.");
      }
    } finally {
      setChargement(false);
    }
  }

  return (
    <div className="auth-page">
      <h1>{mode === "login" ? "Connexion" : "Créer un compte"}</h1>

      <form onSubmit={handleSubmit}>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <label htmlFor="password">Mot de passe</label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          minLength={6}
        />

        {erreur && <p className="erreur">{erreur}</p>}

        <button type="submit" disabled={chargement}>
          {chargement ? "Veuillez patienter..." : mode === "login" ? "Se connecter" : "S'inscrire"}
        </button>
      </form>

      <button
        type="button"
        className="lien-bascule"
        onClick={() => {
          setMode(mode === "login" ? "register" : "login");
          setErreur(null);
        }}
      >
        {mode === "login" ? "Pas encore de compte ? S'inscrire" : "Déjà un compte ? Se connecter"}
      </button>
    </div>
  );
}

export default LoginPage;