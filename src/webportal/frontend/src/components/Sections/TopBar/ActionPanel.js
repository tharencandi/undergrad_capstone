import Button from "components/UI/Button";
import Modal from "components/Modals";
import UploadModalContent from "components/Modals/UploadModal";

import { useState, useRef } from "react";
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
    setUploadError,
  ] = useUploadSVS();

  let workInProgress = false;

  const inputRef = useRef();
  const manifestRef = useRef();

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
    if (numberToUpload !== 0 || uploadError) {
      workInProgress = true;
    }
  }

  const uploadFileChangeHandler = (e) => {
    const files = [...e.target.files];
    setUploadQueue(files);
    if (inputRef.current) {
      inputRef.current.value = "";
    }
    console.log(files);
  };

  const manifestFileChangeHandler = async (e) => {
    // upload e.target.file
    let formData = new FormData();
    formData.append("file", e.target.files[0]);

    await axios
      .post("/automateddownload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then(() => {
        setUploadError(null);
      })
      .catch((err) => {
        console.log(err);
        if (err.response.status === 400) {
          setUploadError("Manifest upload failed: Bad format for manifest");
        } else {
          setUploadError("Problem uploading manifest");
        }
      });

    if (manifestRef.current) {
      manifestRef.current.value = "";
    }
  };

  return (
    <div className="grid grid-cols-2 lg:flex justify-evenly gap-4 xl:gap-6">
      <div className="relative overflow-hidden inline-block cursor-pointer">
        <Button variant="highlight" disabled={numberToUpload > 0}>
          Upload SVS
        </Button>
        <input
          accept=".svs"
          multiple
          type="file"
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
          onChange={uploadFileChangeHandler}
          ref={inputRef}
        />
      </div>
      <div className="relative overflow-hidden inline-block md:mr-6 xl:mr-12 cursor-pointer">
        <Button variant="highlight" disabled={numberToUpload > 0}>
          Manifest
        </Button>
        <input
          type="file"
          ref={manifestRef}
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
          onChange={manifestFileChangeHandler}
        />
      </div>
      <Button
        onClick={() => {
          setModalVariant("generate");
        }}
        disabled={
          selectedData.length === 0 || numberToUpload > 0 ? true : false
        }
      >
        Generate
      </Button>
      <Button
        onClick={() => {
          setModalVariant("delete");
        }}
        disabled={
          selectedData.length === 0 || numberToUpload > 0 ? true : false
        }
      >
        Delete
      </Button>
      <Tooltip title="Cancel all work in progress and reset errors" arrow>
        <div>
          <Button
            onClick={() => {
              setUploadQueue([]);
              setUploadError(null);
              axios
                .get("/cancel")
                .then(() => {})
                .catch((err) => {
                  console.log(err);
                });
            }}
            danger
            hidden={!workInProgress}
          >
            Cancel
          </Button>
        </div>
      </Tooltip>

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
