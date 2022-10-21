import { ReactComponent as DownloadReadyIcon } from "assets/icons/downloadReady.svg";
import useServerAction from "hooks/useServerAction";
import { Tooltip } from "@mui/material";

const DownloadButton = ({ cellId, field }) => {
  const requestServerAction = useServerAction();

  const downloadHandler = () => {
    requestServerAction([cellId], [field], "download", false);
  };

  return (
    <Tooltip title="Click to download" arrow placement="right">
      <button onClick={downloadHandler} className="hover:scale-[1.1]">
        <DownloadReadyIcon />
      </button>
    </Tooltip>
  );
};

export default DownloadButton;
