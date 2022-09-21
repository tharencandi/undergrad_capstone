import { DataGrid } from "@mui/x-data-grid";
import { ReactComponent as DownloadReadyIcon } from "assets/icons/downloadReady.svg";
import { ReactComponent as ProcessingIcon } from "assets/icons/processing.svg";
import { ReactComponent as WaitingIcon } from "assets/icons/waiting.svg";
import { ReactComponent as EditIcon } from "assets/icons/editIcon.svg";
import { v4 as uuidv4 } from "uuid";

import useGetData from "hooks/useGetData";

function filenameCell(cell) {
  return (
    <div className="filenameCell">
      {cell.value}
      <EditIcon />
    </div>
  );
}

function getChildFileStatus(cell) {
  if (cell.value === 0) {
    return "";
  } else if (cell.value === 1) {
    return <DownloadReadyIcon />;
  } else if (cell.value === 2) {
    return <ProcessingIcon></ProcessingIcon>;
  } else if (cell.value === 3) {
    return <WaitingIcon></WaitingIcon>;
  }
}

const columns = [
  {
    field: "filename",
    headerName: "Filename",
    width: 256,
    editable: true,
    renderCell: filenameCell,
  },
  {
    field: "tif",
    headerName: ".tif",
    width: 128,
    renderCell: getChildFileStatus,
  },
  {
    field: "png",
    headerName: ".png",
    width: 128,
    renderCell: getChildFileStatus,
  },
  {
    field: "mask",
    headerName: "Mask",
    width: 128,
    renderCell: getChildFileStatus,
  },
  {
    field: "dateCreated",
    headerName: "Date created",
    description: "This column has a value getter and is not sortable.",
    width: 512,
  },
];

const rows = [
  {
    id: 1,
    filename: "example1.svs",
    tif: 3,
    png: 3,
    mask: 3,
    dateCreated: new Date(2022, 6, 8),
  },
  {
    id: 2,
    filename: "example2.svs",
    tif: 3,
    png: 3,
    mask: 3,
    dateCreated: new Date(2022, 6, 8),
  },
  {
    id: 3,
    filename: "example3.svs",
    tif: 3,
    png: 3,
    mask: 3,
    dateCreated: new Date(2022, 6, 8),
  },
  {
    id: 4,
    filename: "example4.svs",
    tif: 0,
    png: 3,
    mask: 3,
    dateCreated: new Date(2022, 7, 16),
  },
  {
    id: 5,
    filename: "example5.svs",
    tif: 0,
    png: 3,
    mask: 3,
    dateCreated: new Date(2022, 7, 16),
  },
  {
    id: 6,
    filename: "example6.svs",
    tif: 0,
    png: 3,
    mask: 2,
    dateCreated: new Date(2022, 7, 16),
  },
  {
    id: 7,
    filename: "example7.svs",
    tif: 0,
    png: 3,
    mask: 1,
    dateCreated: new Date(2022, 8, 24),
  },
  {
    id: 8,
    filename: "example8.svs",
    tif: 0,
    png: 3,
    mask: 1,
    dateCreated: new Date(2022, 8, 24),
  },
  {
    id: 9,
    filename: "example8.svs",
    tif: 0,
    png: 3,
    mask: 1,
    dateCreated: new Date(2022, 8, 24),
  },
];

const FileTable = () => {
  const data = useGetData();
  console.log(data);
  const rows = data
    ? data.map((entry) => {
        const tif = entry[1].includes("tif") ? 1 : 0;
        const mask = entry[1].includes("svs") ? 1 : 0;
        const png = entry[1].includes("png") ? 1 : 0;

        return {
          id: uuidv4(),
          filename: entry[0],
          tif,
          mask,
          png,
          dateCreated: entry[2],
        };
      })
    : [];

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
