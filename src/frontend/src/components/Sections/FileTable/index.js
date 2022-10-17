import { DataGrid } from "@mui/x-data-grid";
import { ReactComponent as DownloadReadyIcon } from "assets/icons/downloadReady.svg";
import { ReactComponent as ProcessingIcon } from "assets/icons/processing.svg";
import { ReactComponent as WaitingIcon } from "assets/icons/waiting.svg";
import { ReactComponent as EditIcon } from "assets/icons/editIcon.svg";

import { useDispatch } from "react-redux";
import { setSelectedData } from "store/selectedDataReducer";

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
  } else if (cell.value === 2) {
    return <DownloadReadyIcon />;
  } else if (cell.value === 3) {
    return <ProcessingIcon></ProcessingIcon>;
  } else if (cell.value === 1) {
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

const DUMMY_DATA = {
  123: {
    fileId: "123",
    fileName: "example1",
    created: "3rd December 2021",
    tifStatus: "pending",
    pngStatus: "completed",
    maskStatus: "completed",
    downloadStatus: "none",
  },
  456: {
    fileId: "456",
    fileName: "example2",
    created: "2nd December 2021",
    tifStatus: "inProgress",
    pngStatus: "completed",
    maskStatus: "completed",
    downloadStatus: "none",
  },
};

const FileTable = () => {
  useGetData();
  // const data = useSelector((state) => state.data);

  const dispatch = useDispatch();
  const data = DUMMY_DATA;

  const rows = data
    ? Object.keys(data).map((fileKey) => {
        const fileStatusGenerator = (status) => {
          if (status === "none") {
            return 0;
          }
          if (status === "pending") {
            return 1;
          }
          if (status === "completed") {
            return 2;
          }
          return 3;
        };

        const { fileId, fileName, maskStatus, pngStatus, tifStatus, created } =
          data[fileKey];

        return {
          id: fileId,
          filename: fileName,
          tif: fileStatusGenerator(tifStatus),
          mask: fileStatusGenerator(maskStatus),
          png: fileStatusGenerator(pngStatus),
          dateCreated: created,
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
        onSelectionModelChange={(selection) => {
          dispatch(setSelectedData(selection));
        }}
      />
    </div>
  );
};

export default FileTable;
