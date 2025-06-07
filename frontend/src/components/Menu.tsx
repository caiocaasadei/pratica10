import MenuItem from "./MenuItem";

interface MenuProps {
  itens: { label: string; rota: string }[];
}

export default function Menu({ itens }: MenuProps) {
  return (
    <div
      className={`
            flex flex-col justify-start items-center w-52 h-full
            bg-gray-200 rounded-lg text-base
        `}
    >
      {itens.map((item, index) => (
        <MenuItem key={index} label={item.label} rota={item.rota} />
      ))}
    </div>
  );
}
