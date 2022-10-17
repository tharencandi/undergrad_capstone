const InfoBoxCell = ({ icon, text }) => {
  return (
    <div className="px-1 flex flex-col justify-end gap-2 items-center max-w-[90px] py-2">
      <div>{icon}</div>
      <p className="body2 text-center">{text}</p>
    </div>
  );
};

export default InfoBoxCell;
