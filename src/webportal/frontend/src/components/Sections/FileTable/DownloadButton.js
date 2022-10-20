import { ReactComponent as DownloadReadyIcon } from "assets/icons/downloadReady.svg";
import useServerAction from "hooks/useServerAction";

const DownloadButton = ({ cellId, field }) => {
  const requestServerAction = useServerAction();

  const downloadHandler = () => {
    requestServerAction([cellId], [field], "download", false);
  };

  return (
    <button onClick={downloadHandler} className="hover:scale-[1.1]">
      <DownloadReadyIcon />
    </button>
  );
};

export default DownloadButton;
