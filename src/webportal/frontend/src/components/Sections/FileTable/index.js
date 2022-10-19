import { DataGrid } from "@mui/x-data-grid";
import { ReactComponent as DownloadReadyIcon } from "assets/icons/downloadReady.svg";
import { ReactComponent as ProcessingIcon } from "assets/icons/processing.svg";
import { ReactComponent as WaitingIcon } from "assets/icons/waiting.svg";
import { ReactComponent as EditIcon } from "assets/icons/editIcon.svg";

import { useDispatch } from "react-redux";
import { setSelectedData } from "store/selectedDataReducer";
import { useSelector } from "react-redux";
import { useEffect, useState, useCallback } from "react";

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

const FileTable = () => {
  const fetchData = useGetData();
  const [response, setResponse] = useState(0);

  const data = useSelector((state) => state.data);

  const dispatch = useDispatch();

  const dataFetch = useCallback(async () => {
    await fetchData();
    setResponse((prevState) => {
      return prevState + 1;
    });
  }, [fetchData]);

  useEffect(() => {
    let timerId = null;
    if (response) {
      timerId = setTimeout(dataFetch, 2000);
    } else {
      timerId = dataFetch();
    }

    return () => {
      clearTimeout(timerId);
    };
  }, [response, dataFetch]);

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
