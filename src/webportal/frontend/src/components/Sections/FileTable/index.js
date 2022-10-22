import { ReactComponent as ProcessingIcon } from "assets/icons/processing.svg";
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
          ".tif": fileStatusGenerator(tifStatus),
          mask: fileStatusGenerator(maskStatus),
          ".png": fileStatusGenerator(pngStatus),
          dateCreated: created,
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
    }
  }

  const columns = [
    {
      field: "filename",
      headerName: "Filename",
      width: 512,
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
      field: "dateCreated",
      headerName: "Date created",
      description: "This column has a value getter and is not sortable.",
      width: 512,
    },
  ];

  return (
    <div className="fileTable">
      {editMode && (
        <NameChangeModal
          modalController={setEditMode}
          cell={editMode}
        ></NameChangeModal>
      )}
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
