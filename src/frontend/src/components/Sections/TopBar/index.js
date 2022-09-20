import Button from '@mui/material/Button';
import { IconContext } from "react-icons";
import { BsThreeDots, BsHourglassSplit, BsFileEarmarkCheckFill } from "react-icons/bs";

const TopBar = () => {
  return (
    <>
    <div className="topBar">
      <Button variant="contained" component="label">
        Upload SVS
        <input hidden accept="image/*" multiple type="file" />
      </Button>
      <Button variant="contained">Download</Button>
      <Button variant="contained">Generate</Button>
      <Button variant="contained">Delete</Button>
      <div className="infoBox">
        <div className="infoBoxCell"><center><BsThreeDots /></center><span className="caption">Waiting</span></div>
        <div className="infoBoxCell"><center><BsHourglassSplit /></center>Processing</div>
        <div className="infoBoxCell">
          <center>
            <IconContext.Provider value={{ color: "#1665F5" }}>
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
