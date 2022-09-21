const InfoBoxCell = ({ icon, text }) => {
  return (
    <div className="p-1 flex flex-col justify-end gap-2 items-center max-w-[90px] pb-2">
      <div>{icon}</div>
      <p className="body2 text-center">{text}</p>
    </div>
  );
};

export default InfoBoxCell;
