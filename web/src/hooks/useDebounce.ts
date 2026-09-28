import { useState, useEffect } from "react";

function useDebounce<T>(valeur: T, delai: number = 400): T {
  const [valeurDebounced, setValeurDebounced] = useState<T>(valeur);

  useEffect(() => {
    const timer = setTimeout(() => {
      setValeurDebounced(valeur);
    }, delai);

    return () => clearTimeout(timer);
  }, [valeur, delai]);

  return valeurDebounced;
}

export default useDebounce;