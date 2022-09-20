import { useTabsList } from "@mui/base";
import { DataGrid, GridColDef, GridValueGetterParams } from "@mui/x-data-grid";
import { IconContext } from "react-icons";
import { BsFillPencilFill, BsThreeDots, BsHourglassSplit, BsFileEarmarkCheckFill } from "react-icons/bs";

function filenameCell(params) {
  return (
    <div style={{width: "100%"}}>
      {params.row.filename}
      <span style={{float: "right"}}>
        <BsFillPencilFill />
      </span>
    </div>
  )
}

function getTifStatus(params) {
  if (params.row.tif === 0) {
    return ""
  } else if (params.row.tif === 1) {
    return <BsThreeDots />
  } else if (params.row.tif === 2) {
    return <BsHourglassSplit />
  } else if (params.row.tif === 3) {
    return (
      <IconContext.Provider value={{ color: "#1665F5" }}>
        <BsFileEarmarkCheckFill />
      </IconContext.Provider>
    )
  }
}

function getPngStatus(params) {
  if (params.row.png === 0) {
    return ""
  } else if (params.row.png === 1) {
    return <BsThreeDots />
  } else if (params.row.png === 2) {
    return <BsHourglassSplit />
  } else if (params.row.png === 3) {
    return (
      <IconContext.Provider value={{ color: "#1665F5" }}>
        <BsFileEarmarkCheckFill />
      </IconContext.Provider>
    )
  }
}

function getMaskStatus(params) {
  if (params.row.mask === 0) {
    return ""
  } else if (params.row.mask === 1) {
    return <BsThreeDots />
  } else if (params.row.mask === 2) {
    return <BsHourglassSplit />
  } else if (params.row.mask === 3) {
    return (
      <IconContext.Provider value={{ color: "#1665F5" }}>
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
    renderCell: getTifStatus
  },
  {
    field: "png",
    headerName: ".png",
    width: 128,
    renderCell: getPngStatus
  },
  {
    field: "mask",
    headerName: "Mask",
    width: 128,
    renderCell: getMaskStatus
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
    <div style={{ height: "80vh", width: "100%" }}>
      <DataGrid
        rows={rows}
        columns={columns}
        pageSize={100}
        rowsPerPageOptions={[5]}
        checkboxSelection
      />
    </div>
  );
};

export default FileTable;
