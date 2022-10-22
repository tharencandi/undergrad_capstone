import ReactDOM from "react-dom";
import CheckboxList from "./CheckList";
import Button from "components/UI/Button";
import React, { useState, useEffect } from "react";
import { useSelector } from "react-redux";
import useServerAction from "hooks/useServerAction";
import useGetData from "hooks//useGetData";
import OverwriteOption from "./OverwriteOption";

const Backdrop = ({ modalController }) => {
  return (
    <div
      className="absolute inset-0 w-screen h-screen bg-black bg-opacity-70 flex justify-center items-center"
      onClick={() => {
        modalController("none");
      }}
    ></div>
  );
};

const Overlay = ({ variant, modalController }) => {
  const [checked, setChecked] = React.useState([]);
  const [overwrite, setOverwrite] = React.useState([]);
  const allData = useSelector((state) => {
    return state.data;
  });

  const selectedData = useSelector((state) => state.selectedData);
  const requestServerAction = useServerAction();
  const fetchData = useGetData();
  const [warningMessage, setWarningMessage] = useState("");

  // On each render, check that the selected data has all the extensions ready for download
  useEffect(() => {
    (async () => {
      await fetchData();

      const checkedMap = {
        ".tif": "tifStatus",
        ".png": "pngStatus",
        mask: "maskStatus",
      };

      let unavailableTypes = [];
      if (variant === "download") {
        // For each selected file
        selectedData.forEach((selection) => {
          // Check to see if the checked option is ready for download
          checked.forEach((checkedOption) => {
            if (
              allData[selection][checkedMap[checkedOption]] !== "completed" &&
              checkedOption !== ".svs"
            ) {
              unavailableTypes.push(checkedOption);
            }
          });
        });

        unavailableTypes = [...new Set(unavailableTypes)];
        unavailableTypes = unavailableTypes.map((type) => {
          if (type[0] === ".") {
            return `"${type.slice(1)}"`;
          }
          return `"${type}"`;
        });

        unavailableTypes = unavailableTypes.join(", ");

        setWarningMessage(
          unavailableTypes.length > 0
            ? `Not all selected files for extensions ${unavailableTypes} are available for download. Only those that are ready will be downloaded.`
            : ""
        );
        return;
      }

      if (variant === "delete") {
        // For each selected file
        selectedData.forEach((selection) => {
          // Check to see if the checked option is ready for download
          checked.forEach((checkedOption) => {
            if (
              allData[selection][checkedMap[checkedOption]] !== "completed" &&
              checkedOption !== ".svs"
            ) {
              unavailableTypes.push(checkedOption);
            }
          });
        });

        unavailableTypes = [...new Set(unavailableTypes)];
        unavailableTypes = unavailableTypes.map((type) => {
          if (type[0] === ".") {
            return `"${type.slice(1)}"`;
          }
          return `"${type}"`;
        });

        unavailableTypes = unavailableTypes.join(", ");

        if (checked.includes(".svs")) {
          setWarningMessage(
            'You have selected ".svs", which will delete the entire entry including ALL "tif", "png" and masks associated with those files.'
          );
          return;
        }

        setWarningMessage(
          unavailableTypes.length > 0
            ? `Not all files selected for extensions ${unavailableTypes} are available to delete. Only those that are ready will be deleted.`
            : ""
        );
        return;
      }

      if (variant === "generate") {
        // For each selected file
        selectedData.forEach((selection) => {
          // Check to see if the checked option is already generated
          checked.forEach((checkedOption) => {
            if (allData[selection][checkedMap[checkedOption]] !== "none") {
              unavailableTypes.push(checkedOption);
            }
          });
        });

        unavailableTypes = [...new Set(unavailableTypes)];
        unavailableTypes = unavailableTypes.map((type) => {
          if (type[0] === ".") {
            return `"${type.slice(1)}"`;
          }
          return `"${type}"`;
        });

        unavailableTypes = unavailableTypes.join(", ");

        setWarningMessage(
          unavailableTypes.length > 0
            ? `Some of the requested files for generation: ${unavailableTypes} are already generated or pending generation. Would you like to overwrite existing files? If not selected, only files which have not previously been generated will be processed.`
            : ""
        );
        return;
      }
    })();
  }, [fetchData, checked, selectedData, variant]);

  return (
    <div className="absolute inset-0 min-w-[400px] max-w-[750px] h-[500px] m-auto bg-white p-8 rounded-sm z-10 flex flex-col">
      <h2 className="subtitle1">
        {selectedData.length} {selectedData.length === 1 ? "file" : "files"}{" "}
        selected to {variant}:{" "}
        <span className="text-red">
          {variant === "delete" ? "(cannot be undone)" : ""}
        </span>
      </h2>
      <CheckboxList
        checked={checked}
        setChecked={setChecked}
        variant={variant}
      ></CheckboxList>
      <div className="flex flex-grow flex-col justify-end pb-4">
        <p className="warning">
          <span className="subtitle2">{warningMessage && "WARNING:"} </span>
          {warningMessage}
        </p>
        {warningMessage && variant === "generate" && (
          <OverwriteOption
            checked={overwrite}
            setChecked={setOverwrite}
          ></OverwriteOption>
        )}
      </div>
      <div className="flex items-end justify-between">
        <Button
          onClick={() => {
            modalController("none");
          }}
        >
          Cancel
        </Button>
        {/* Submit Button */}
        <Button
          variant="highlight"
          danger={variant === "delete" ? true : false}
          disabled={checked.length > 0 ? false : true}
          onClick={() => {
            requestServerAction(
              selectedData,
              checked,
              variant,
              overwrite.length > 0 ? true : false
            );
          }}
        >
          {variant[0].toUpperCase() + variant.substring(1)}
        </Button>
      </div>
    </div>
  );
};

// The variant is the delete, download or generate variant
const Modal = ({ variant, modalController }) => {
  return (
    <>
      {ReactDOM.createPortal(
        <Overlay variant={variant} modalController={modalController}></Overlay>,
        document.getElementById("overlay-root")
      )}
      {ReactDOM.createPortal(
        <Backdrop modalController={modalController}></Backdrop>,
        document.getElementById("backdrop-root")
      )}
    </>
  );
};

export default Modal;
