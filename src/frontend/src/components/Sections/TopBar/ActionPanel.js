import Button from "components/UI/Button";
import Modal from "components/Modals";
import UploadModalContent from "components/Modals/UploadModal";

import { useState } from "react";
import useUploadSVS from "hooks/useUploadSVS";
import useDownload from "hooks/useDownload";
import useGenerate from "hooks/useGenerate";

const ActionPanel = () => {
  // Modal variants - "download", "generate", "none" (none means no modal open)
  const [modalVariant, setModalVariant] = useState("none");
  const [
    setUploadQueue,
    uploadProgress,
    currentUploadingFile,
    numberUploaded,
    numberToUpload,
  ] = useUploadSVS();

  const uploadFileChangeHandler = (e) => {
    setUploadQueue(e.target.files);
  };

  const requestDownload = useDownload();
  const requestGenerate = useGenerate();

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
      <Button>Delete</Button>
      {modalVariant === "none" ? null : (
        <Modal
          modalController={setModalVariant}
          variant={modalVariant}
          downloadHandler={requestDownload}
          generateHandler={requestGenerate}
        ></Modal>
      )}
      {numberToUpload > 0 ? (
        <UploadModalContent
          numberToUpload={numberToUpload}
          uploadProgress={uploadProgress}
          currentUploadingFile={currentUploadingFile}
          numberUploaded={numberUploaded}
        ></UploadModalContent>
      ) : null}
    </div>
  );
};

export default ActionPanel;
