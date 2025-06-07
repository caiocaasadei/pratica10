interface InputProps {
  label: string;
  type: string;
  name: string;
  value?: string | number;
  onChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
  erro?: string;
  onBlur: (event: React.FocusEvent<HTMLInputElement>) => void;
  onFocus: (event: React.FocusEvent<HTMLInputElement>) => void;
}

const InputCadastro = ({
  label,
  type,
  name,
  value,
  onChange,
  onBlur,
  onFocus,
  erro,
}: InputProps) => {
  return (
    <div className="mb-1">
      <label
        htmlFor={name}
        className="block text-sm font-medium text-gray-700 mb-1"
      >
        {label}
      </label>
      <input
        type={type}
        id={name}
        name={name}
        value={value}
        onChange={onChange}
        onBlur={onBlur}
        onFocus={onFocus}
        className={`w-full  px-3 py-1 border rounded-md shadow-sm text-base focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
          erro ? "border-red-500" : "border-gray-300"
        }`}
      />
      {erro && <div className="text-red-600 text-sm mt-1">{erro}</div>}
    </div>
  );
};

export default InputCadastro;
