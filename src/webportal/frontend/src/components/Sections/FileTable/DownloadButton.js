import { ReactComponent as DownloadReadyIcon } from "assets/icons/downloadReady.svg";
import { ReactComponent as DownloadErrorIcon } from "assets/icons/downloadError.svg";

import useServerAction from "hooks/useServerAction";
import { Tooltip } from "@mui/material";
import { useState } from "react";

const DownloadButton = ({ cellId, field }) => {
  const requestServerAction = useServerAction();

  const downloadHandler = () => {
    requestServerAction([cellId], [field], "download", false)
      .then(() => {
        setError(null);
      })
      .catch((err) => {
        setError(err.message);
      });
  };

  const [error, setError] = useState(null);

  return (
    <>
      <Tooltip
        title={error ? `${error}. Click to retry.` : "Click to Download"}
        arrow
        placement="right"
      >
        <button onClick={downloadHandler} className="hover:scale-[1.1]">
          {error ? (
            <DownloadErrorIcon></DownloadErrorIcon>
          ) : (
            <DownloadReadyIcon />
          )}
        </button>
      </Tooltip>
    </>
  );
};

export default DownloadButton;
