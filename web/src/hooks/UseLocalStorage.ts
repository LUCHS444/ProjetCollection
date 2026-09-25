import { useState } from "react";

function useLocalStorage<T>(
  key: string,
  valeurInitiale: T
): [T, (v: T) => void] {
  const [valeur, setValeur] = useState<T>(() => {
    try {
      const stocke = window.localStorage.getItem(key);
      return stocke !== null ? (JSON.parse(stocke) as T) : valeurInitiale;
    } catch {
      return valeurInitiale;
    }
  });

  const setStoredValue = (v: T): void => {
    try {
      setValeur(v);
      window.localStorage.setItem(key, JSON.stringify(v));
    } catch {
      // stockage indisponible (mode privé, quota dépassé...) : on ignore silencieusement
    }
  };

  return [valeur, setStoredValue];
}

export default useLocalStorage;