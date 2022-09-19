import Button from '@mui/material/Button';

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
    </div>
    </>
  );
};

export default TopBar;
