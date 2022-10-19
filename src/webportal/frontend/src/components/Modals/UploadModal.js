import ReactDOM from "react-dom";

const UploadModalContent = ({
  numberToUpload,
  currentUploadingFile,
  numberUploaded,
}) => {
  return ReactDOM.createPortal(
    <div className="absolute bottom-8 left-8 h-[150px] w-[400px] bg-white p-4 border-[1px] rounded-sm">
      <p>
        Uploaded {numberUploaded} out of {numberToUpload}.
      </p>
      <p>Currently uploading: {currentUploadingFile}</p>
    </div>,
    document.getElementById("upload-modal-root")
  );
};

export default UploadModalContent;
