const Button = ({ children, variant }) => {
  const baseStyle =
    "w-[160px] h-[60px] px-4 py-2 bg-primary text-subtitle1 rounded-[2px]  cursor-pointer";

  const variantStyle =
    variant === "highlight"
      ? "bg-primary text-white"
      : "bg-secondary text-black";

  return <button className={`${baseStyle} ${variantStyle}`}>{children}</button>;
};

export default Button;
