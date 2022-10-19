const Button = ({ children, variant, onClick, disabled, danger }) => {
  const baseStyle =
    "w-[130px] h-[50px] xl:w-[160px] xl:h-[60px] px-4 py-2 bg-primary text-subtitle2 xl:text-subtitle1 rounded-[2px]  cursor-pointer";

  const variantStyle =
    variant === "highlight"
      ? "bg-primary text-white"
      : "bg-secondary text-black";

  const dangerStyle = "bg-red text-white";

  const disabledStyle = disabled ? "opacity-50 cursor-default" : "";

  return (
    <button
      className={`${baseStyle} ${
        danger ? dangerStyle : variantStyle
      } ${disabledStyle}`}
      onClick={disabled ? null : onClick}
    >
      {children}
    </button>
  );
};

export default Button;
