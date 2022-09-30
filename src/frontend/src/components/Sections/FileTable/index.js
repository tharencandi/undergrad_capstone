import Button from '@mui/material/Button';
import { useTabsList } from "@mui/base";
import { DataGrid, GridColDef, GridValueGetterParams } from "@mui/x-data-grid";
import { IconContext } from "react-icons";
import { BsFillPencilFill, BsThreeDots, BsHourglassSplit, BsFileEarmarkCheckFill } from "react-icons/bs";

function filenameCell(cell) {
  return (
    <div className="filenameCell">
      {cell.value}
      <Button variant="text"><BsFillPencilFill /></Button>
    </div>
  )
}

function getChildFileStatus(cell) {
  if (cell.value === 0) {
    return ""
  } else if (cell.value === 1) {
    return (
      <IconContext.Provider value={{ className: "waitingIcon" }}>
        <BsThreeDots />
      </IconContext.Provider>
    )
  } else if (cell.value === 2) {
    return (
      <IconContext.Provider value={{ className: "processingIcon" }}>
        <BsHourglassSplit />
      </IconContext.Provider>
    )
  } else if (cell.value === 3) {
    return (
      <IconContext.Provider value={{ className: "readyIcon" }}>
        <BsFileEarmarkCheckFill />
      </IconContext.Provider>
    )
  }
}

const columns: GridColDef[] = [
  {
    field: "filename",
    headerName: "Filename",
    width: 256,
    editable: true,
    renderCell: filenameCell
  },
  {
    field: "tif",
    headerName: ".tif",
    width: 128,
    renderCell: getChildFileStatus
  },
  {
    field: "png",
    headerName: ".png",
    width: 128,
    renderCell: getChildFileStatus
  },
  {
    field: "mask",
    headerName: "Mask",
    width: 128,
    renderCell: getChildFileStatus
  },
  {
    field: "dateCreated",
    headerName: "Date created",
    description: "This column has a value getter and is not sortable.",
    width: 192
  }
];

const rows = [
  { id: 1, filename: "example1", tif: 3, png: 3, mask: 3, dateCreated: new Date(2022, 6, 8) },
  { id: 2, filename: "example2", tif: 3, png: 3, mask: 3, dateCreated: new Date(2022, 6, 8) },
  { id: 3, filename: "example3", tif: 3, png: 3, mask: 3, dateCreated: new Date(2022, 6, 8) },
  { id: 4, filename: "example4", tif: 0, png: 3, mask: 3, dateCreated: new Date(2022, 7, 16) },
  { id: 5, filename: "example5", tif: 0, png: 3, mask: 3, dateCreated: new Date(2022, 7, 16) },
  { id: 6, filename: "example6", tif: 0, png: 3, mask: 2, dateCreated: new Date(2022, 7, 16) },
  { id: 7, filename: "example7", tif: 0, png: 3, mask: 1, dateCreated: new Date(2022, 8, 24) },
  { id: 8, filename: "example8", tif: 0, png: 3, mask: 1, dateCreated: new Date(2022, 8, 24) },
  { id: 9, filename: "example8", tif: 0, png: 3, mask: 1, dateCreated: new Date(2022, 8, 24) },
];

const FileTable = () => {
  return (
    <div className="fileTable">
      <DataGrid
        rows={rows}
        columns={columns}
        pageSize={100}
        rowsPerPageOptions={[5]}
        checkboxSelection
        disableSelectionOnClick
      />
    </div>
  );
};

export default FileTable;
