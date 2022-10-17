const Button = ({ children, variant, onClick }) => {
  const baseStyle =
    "w-[130px] h-[50px] xl:w-[160px] xl:h-[60px] px-4 py-2 bg-primary text-subtitle2 xl:text-subtitle1 rounded-[2px]  cursor-pointer";

  const variantStyle =
    variant === "highlight"
      ? "bg-primary text-white"
      : "bg-secondary text-black";

  return (
    <button className={`${baseStyle} ${variantStyle}`} onClick={onClick}>
      {children}
    </button>
  );
};

export default Button;
