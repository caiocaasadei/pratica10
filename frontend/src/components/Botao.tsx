import React from "react";

interface BotaoProps {
  titulo: string;
  onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void; // Opcional: função para eventos de clique
}

const Botao: React.FC<BotaoProps> = ({ titulo, onClick }) => {
  return (
    <button
      onClick={onClick}
      className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition"
    >
      {titulo}
    </button>
  );
};

export default Botao;
