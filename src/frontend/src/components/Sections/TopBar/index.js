import Button from '@mui/material/Button';
import { IconContext } from "react-icons";
import { BsThreeDots, BsHourglassSplit, BsFileEarmarkCheckFill } from "react-icons/bs";

const TopBar = () => {
  return (
    <>
    <div className="topBar">
      <div className="actionPanel">
        <Button variant="contained" component="label">
          Upload SVS
          <input hidden accept="image/*" multiple type="file" />
        </Button>
        <Button variant="contained">Download</Button>
        <Button variant="contained">Generate</Button>
        <Button variant="contained">Delete</Button>
      </div>
      <div className="infoBox">
        <div className="infoBoxCell">
          <center>
            <IconContext.Provider value={{ className: "waitingIcon" }}>
              <BsThreeDots />
            </IconContext.Provider>
          </center>
          Waiting
        </div>
        <div className="infoBoxCell">
          <center>
            <IconContext.Provider value={{ className: "processingIcon" }}>
              <BsHourglassSplit />
            </IconContext.Provider>
          </center>
          Processing
        </div>
        <div className="infoBoxCell">
          <center>
            <IconContext.Provider value={{ className: "readyIcon" }}>
              <BsFileEarmarkCheckFill />
            </IconContext.Provider>
          </center>
          Ready
        </div>
      </div>
    </div>
    </>
  );
};

export default TopBar;
