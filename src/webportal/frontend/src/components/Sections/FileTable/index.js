import { ReactComponent as ErrorIcon } from "assets/icons/statusError.svg";
import { ReactComponent as WaitingIcon } from "assets/icons/waiting.svg";
import { ReactComponent as EditIcon } from "assets/icons/editIcon.svg";
import loadingGif from "assets/icons/loading-load.gif";

import { DataGrid } from "@mui/x-data-grid";
import { Tooltip } from "@mui/material";

import DownloadButton from "./DownloadButton";

import { useDispatch } from "react-redux";
import { setSelectedData } from "store/selectedDataReducer";
import { useSelector } from "react-redux";
import { useEffect, useState, useCallback } from "react";

import useGetData from "hooks/useGetData";

import NameChangeModal from "../../Modals/NameChangeModal";

const FileTable = () => {
  const fetchData = useGetData();
  const [response, setResponse] = useState(0);

  const [editMode, setEditMode] = useState(null);

  const [error, setError] = useState(null);

  const data = useSelector((state) => state.data);

  const dispatch = useDispatch();

  const dataFetch = useCallback(async () => {
    await fetchData()
      .then(() => {
        setError(null);
      })
      .catch((err) => {
        setError(err);
      });
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
          if (status === "inProgress") {
            return 3;
          }
          return status;
        };

        const {
          fileId,
          fileName,
          maskStatus,
          pngStatus,
          tifStatus,
          created,
          caseType,
        } = data[fileKey];

        return {
          id: fileId,
          filename: fileName,
          ".tif": fileStatusGenerator(tifStatus),
          mask: fileStatusGenerator(maskStatus),
          ".png": fileStatusGenerator(pngStatus),
          dateCreated: created,
          caseType,
        };
      })
    : [];

  function filenameCell(cell) {
    return (
      <div className="filenameCell">
        {`${cell.value}.svs`}
        <Tooltip title="Edit Name" arrow>
          <button
            onClick={() => {
              setEditMode(cell);
            }}
            className="hover:scale-[1.1]"
          >
            <EditIcon></EditIcon>
          </button>
        </Tooltip>
      </div>
    );
  }

  function getChildFileStatus(cell) {
    if (cell.value === 0) {
      return "";
    } else if (cell.value === 2) {
      return <DownloadButton cellId={cell.id} field={cell.field} />;
    } else if (cell.value === 3) {
      return <img src={loadingGif} alt={"loading"} width="75" height="37" />;
    } else if (cell.value === 1) {
      return <WaitingIcon></WaitingIcon>;
    } else {
      return (
        <Tooltip title={cell.value} arrow>
          <ErrorIcon></ErrorIcon>
        </Tooltip>
      );
    }
  }

  const columns = [
    {
      field: "id",
      headerName: "FileID",
      width: 300,
    },
    {
      field: "filename",
      headerName: "Filename",
      width: 650,
      renderCell: filenameCell,
    },
    {
      field: ".tif",
      headerName: ".tif",
      width: 128,
      renderCell: getChildFileStatus,
      align: "center",
    },
    {
      field: ".png",
      headerName: ".png",
      width: 128,
      renderCell: getChildFileStatus,
      align: "center",
    },
    {
      field: "mask",
      headerName: "Mask",
      width: 128,
      renderCell: getChildFileStatus,
      align: "center",
    },
    {
      field: "caseType",
      headerName: "Case",
      width: 128,
    },
    {
      field: "dateCreated",
      headerName: "Date created",
      description: "This column has a value getter and is not sortable.",
      width: 256,
    },
  ];

  return (
    <div className="fileTable">
      {!error && editMode && (
        <NameChangeModal
          modalController={setEditMode}
          cell={editMode}
        ></NameChangeModal>
      )}
      {!error && (
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
      )}
      {error && (
        <p className="warning text-center pt-12">
          An error occured while retrieving data: {error.message}
        </p>
      )}
    </div>
  );
};

export default FileTable;
