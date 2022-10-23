import ReactDOM from "react-dom";

const UploadModalContent = ({
  numberToUpload,
  currentUploadingFile,
  numberUploaded,
}) => {
  return ReactDOM.createPortal(
    <div className="absolute bottom-8 left-8 h-[125px] w-[300px]  bg-white p-4 border-solid border-4 border-secondary rounded">
      <p className="body2">
        Uploaded: <span className="text-primary ">{numberUploaded}</span> out of{" "}
        {numberToUpload}.
      </p>
      <p className="body2">
        Currently uploading:{" "}
        <span className="text-primary">{currentUploadingFile}</span>
      </p>
    </div>,
    document.getElementById("upload-modal-root")
  );
};

export default UploadModalContent;
