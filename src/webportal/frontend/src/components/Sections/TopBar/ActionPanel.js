import Button from "components/UI/Button";
import Modal from "components/Modals";
import UploadModalContent from "components/Modals/UploadModal";

import { useState } from "react";
import useUploadSVS from "hooks/useUploadSVS";
import { useSelector } from "react-redux";

import { Tooltip } from "@mui/material";
import axios from "axios";

const ActionPanel = () => {
  // Modal variants - "download", "generate", "none" (none means no modal open)
  const [modalVariant, setModalVariant] = useState("none");
  const selectedData = useSelector((state) => state.selectedData);
  const data = useSelector((state) => state.data);

  const [
    setUploadQueue,
    currentUploadingFile,
    numberUploaded,
    numberToUpload,
    uploadError,
  ] = useUploadSVS();

  let workInProgress = false;

  for (let entry in data) {
    if (
      data[entry].tifStatus !== "none" &&
      data[entry].tifStatus !== "completed"
    ) {
      workInProgress = true;
    }
    if (
      data[entry].pngStatus !== "none" &&
      data[entry].pngStatus !== "completed"
    ) {
      workInProgress = true;
    }
    if (
      data[entry].maskStatus !== "none" &&
      data[entry].maskStatus !== "completed"
    ) {
      workInProgress = true;
    }
    if (numberToUpload !== 0) {
      workInProgress = true;
    }
  }

  const uploadFileChangeHandler = (e) => {
    setUploadQueue(e.target.files);
  };

  return (
    <div className="grid grid-cols-2 lg:flex justify-evenly gap-4 xl:gap-6">
      <div className="relative overflow-hidden inline-block md:mr-6 xl:mr-12 cursor-pointer">
        <Button variant="highlight">Upload SVS</Button>
        <input
          accept=".svs"
          multiple
          type="file"
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
          onChange={uploadFileChangeHandler}
        />
      </div>
      <Button
        onClick={() => {
          setModalVariant("generate");
        }}
        disabled={selectedData.length === 0 ? true : false}
      >
        Generate
      </Button>
      <Button
        onClick={() => {
          setModalVariant("delete");
        }}
        disabled={selectedData.length === 0 ? true : false}
      >
        Delete
      </Button>
      <Button onClick={() => {}} danger hidden={!workInProgress}>
        Cancel All
      </Button>
      {modalVariant === "none" ? null : (
        <Modal modalController={setModalVariant} variant={modalVariant}></Modal>
      )}
      {numberToUpload > 0 || uploadError ? (
        <UploadModalContent
          numberToUpload={numberToUpload}
          currentUploadingFile={currentUploadingFile}
          numberUploaded={numberUploaded}
          error={uploadError}
        ></UploadModalContent>
      ) : null}
    </div>
  );
};

export default ActionPanel;
