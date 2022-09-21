import InfoBoxCell from "./InfoBoxCell";
import { ReactComponent as DownloadReadyIcon } from "assets/icons/downloadReady.svg";
import { ReactComponent as ProcessingIcon } from "assets/icons/processing.svg";
import { ReactComponent as WaitingIcon } from "assets/icons/waiting.svg";
import { v4 as uuidv4 } from "uuid";

const InfoBox = () => {
  const infoItems = [
    {
      text: "Ready for download",
      icon: <DownloadReadyIcon />,
    },
    {
      text: "Being processed",
      icon: <ProcessingIcon />,
    },
    {
      text: "Waiting to be processed",
      icon: <WaitingIcon />,
    },
  ];

  const infoItemElements = infoItems.map((infoItem) => {
    return <InfoBoxCell {...infoItem} key={uuidv4()}></InfoBoxCell>;
  });

  return (
    <div className="flex justify-evenly px-4 py-1 border-solid border-4 border-secondary rounded gap-4">
      {infoItemElements}
    </div>
  );
};

export default InfoBox;
