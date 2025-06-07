import { Link } from "react-router-dom";
import { useUsuario } from "../contexts/UsuarioContext";  

interface MenuItemProps {
  label: string;
  rota: string;
}

export default function MenuItem({ label, rota }: MenuItemProps) {
  const { setTituloPagina } = useUsuario();;
  const handleClick = () => {
    setTituloPagina(label);
  };

  return (
    <Link
      to={rota}
      onClick={handleClick}
          
      className={`
                block w-full px-3 py-1 text-xl text-white 
                bg-blue-500 hover:bg-zinc-700 
                rounded-md transition-all
                mb-2  /* Adiciona espaçamento entre os itens */
            `}
    >
      {label}
    </Link>
  );
}
