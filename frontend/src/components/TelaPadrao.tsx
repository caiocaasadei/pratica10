import { useEffect, useState, lazy, Suspense } from "react";
import { useRoutes, useLocation } from "react-router-dom";
import Menu from "./Menu";
import Cabecalho from "./Cabecalho";
import Conteudo from "./Conteudo";
import { useUsuario } from "../contexts/UsuarioContext";

import {
  Administrador,
  Func,
  Gestor,
} from "../Menu";

interface MenuItem {
  label: string;
  rota: string;
}

const getMenuJson = (idtPapel: string): MenuItem[] => {
  switch (idtPapel) {
    case "A":
      return Administrador;
    case "F":
      return Func;
    case "G":
      return Gestor;
    default:
      return [];
  }
};

export default function TelaPadrao() {
  const [mostrarMenu, setMostrarMenu] = useState(true);
  const [menuItens, setMenuItens] = useState<MenuItem[]>([]);
  const location = useLocation();
  const { idtPapel, setUsuario } = useUsuario();

  useEffect(() => {
    setMostrarMenu(location.pathname === "/TelaPadrao");
  }, [location.pathname]);

  useEffect(() => {
    const menu = getMenuJson(idtPapel);
    setMenuItens(menu);
  }, [idtPapel, setUsuario]);

  const element = useRoutes([
    {
      path: "/",
      element: <Conteudo />,
      children: menuItens.map(({ rota }) => {
        const Componente = lazy(() => import(`../${rota.substring(1)}/page.tsx`));
        return {
          path: rota.substring(1),
          element: (
            <Suspense fallback={<div>Carregando...</div>}>
              <Componente />
            </Suspense>
          ),
        };
      }),
    },
    {
      path: "*",
      element: <div></div>,
    },
  ]);

  return (
    <div className="h-screen flex flex-col">
      <Cabecalho logado={true} />
      <div className="flex flex-1">
        {mostrarMenu && <Menu itens={menuItens} />}
        <div className="flex-1">
          {element}
        </div>
      </div>
    </div>
  );
}
