import React from "react";

interface BotaoProps {
  titulo: string;
  onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void; // Opcional: função para eventos de clique
  type?: "button" | "submit" | "reset";
}

const Botao: React.FC<BotaoProps> = ({ titulo, onClick }) => {
  return (
    <button
      onClick={onClick}
      className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition"
    >
      {titulo}
    </button>
  );
};

export default Botao;
