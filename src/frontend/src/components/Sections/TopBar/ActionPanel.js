import Button from "components/UI/Button";
import Modal from "components/Modals";
import UploadModalContent from "components/Modals/UploadModal";

import { useState } from "react";
import useUploadSVS from "hooks/useUploadSVS";
import useServerAction from "hooks/useServerAction";
import { useSelector } from "react-redux";

const ActionPanel = () => {
  // Modal variants - "download", "generate", "none" (none means no modal open)
  const [modalVariant, setModalVariant] = useState("none");
  const requestServerAction = useServerAction();
  const selectedData = useSelector((state) => state.selectedData);

  const [setUploadQueue, currentUploadingFile, numberUploaded, numberToUpload] =
    useUploadSVS();

  const uploadFileChangeHandler = (e) => {
    console.log(setUploadQueue);
    setUploadQueue(e.target.files);
  };

  return (
    <div className="grid grid-cols-2 lg:flex justify-evenly gap-4 xl:gap-6">
      <div className="relative overflow-hidden inline-block md:mr-6 xl:mr-12 cursor-pointer">
        <Button variant="highlight">Upload SVS</Button>
        <input
          accept="image/*"
          multiple
          type="file"
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
          onChange={uploadFileChangeHandler}
        />
      </div>
      <Button
        onClick={() => {
          setModalVariant("download");
        }}
      >
        Download
      </Button>
      <Button
        onClick={() => {
          setModalVariant("generate");
        }}
      >
        Generate
      </Button>
      <Button
        onClick={() => {
          requestServerAction(selectedData, null, "delete");
        }}
      >
        Delete
      </Button>
      {modalVariant === "none" ? null : (
        <Modal modalController={setModalVariant} variant={modalVariant}></Modal>
      )}
      {numberToUpload > 0 ? (
        <UploadModalContent
          numberToUpload={numberToUpload}
          currentUploadingFile={currentUploadingFile}
          numberUploaded={numberUploaded}
        ></UploadModalContent>
      ) : null}
    </div>
  );
};

export default ActionPanel;
