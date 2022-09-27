import Button from "components/UI/Button";
import Modal from "components/Modals";
import { useState } from "react";

const ActionPanel = () => {
  // Modal variants - "download", "generate", "none" (none means no modal open)
  const [modalVariant, setModalVariant] = useState("none");

  return (
    <div className="grid grid-cols-2 lg:flex justify-evenly gap-4 xl:gap-6">
      <div className="relative overflow-hidden inline-block md:mr-6 xl:mr-12 cursor-pointer">
        <Button variant="highlight">Upload SVS</Button>
        <input
          accept="image/*"
          multiple
          type="file"
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
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
        <Modal modalController={setModalVariant} variant={modalVariant}></Modal>
      )}
    </div>
  );
};

export default ActionPanel;
