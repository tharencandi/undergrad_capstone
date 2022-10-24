import { useEffect, useState } from "react";
import axios from "axios";

const useUploadSVS = () => {
  const [uploadQueue, setUploadQueue] = useState([]);
  const [currentUploadingFile, setCurrentUploadingFile] = useState(null);
  const [numberUploaded, setNumberUploaded] = useState(0);
  const [numberToUpload, setNumberToUpload] = useState(0);
  const [error, setError] = useState(null);

  //When there have been new files queued, update the global store and trigger an upload
  useEffect(() => {
    const uploadFile = async (file) => {
      let formData = new FormData();
      formData.append("file", file);

      setCurrentUploadingFile(file.name);

      // Delay
      await new Promise((resolve) => setTimeout(resolve, 500));

      const res = await axios
        .post("/scan", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((res) => {
          setError(null);
        })
        .catch((err) => {
          setError(
            `Attempted upload for "${file.name}" failed: ${err.message}`
          );
          throw new Error(err.message);
        });

      setCurrentUploadingFile(null);
      return res;
    };

    // If there is already a file uploading, then do not start another upload
    if (currentUploadingFile) {
      return;
    }

    if (uploadQueue.length > 0) {
      const currentFile = uploadQueue[0];

      uploadFile(currentFile)
        .then((res) => {
          console.log(res);

          setNumberUploaded((prevState) => {
            return prevState + 1;
          });
          setUploadQueue((prevState) => {
            return [...prevState.slice(1)];
          });
        })
        .catch((err) => {
          // Upload cancelled or failed
          console.log(err);
          setNumberUploaded(0);
          setNumberToUpload(0);
          setCurrentUploadingFile(null);
          setUploadQueue([]);
        });
    } else {
      // Nothing queued to upload, then reset the number uploaded
      setNumberUploaded(0);
      setNumberToUpload(0);
      setCurrentUploadingFile(null);
    }
  }, [uploadQueue, currentUploadingFile]);

  // Concatenate the original queue with new files to upload
  return [
    (newFiles) => {
      setNumberToUpload((prevState) => prevState + newFiles.length);
      setUploadQueue((prevState) => [...prevState, ...newFiles]);
    },
    currentUploadingFile,
    numberUploaded,
    numberToUpload,
    error,
  ];
};

export default useUploadSVS;
