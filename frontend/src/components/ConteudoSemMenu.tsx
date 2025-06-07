

export default function ConteudoSemMenu(props: any) {
  return (
    <div
      className={`
        flex justify-start
        h-full
        w-full
        bg-white
        text-black
        g-5
      `}
    >
       {props.children}
    </div>
  );
}