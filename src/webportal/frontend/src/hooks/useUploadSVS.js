import { useEffect, useState } from "react";
import axios from "axios";

const useUploadSVS = () => {
  const [uploadQueue, setUploadQueue] = useState([]);
  const [currentUploadingFile, setCurrentUploadingFile] = useState(null);
  const [numberUploaded, setNumberUploaded] = useState(0);
  const [numberToUpload, setNumberToUpload] = useState(0);
  const [error, setError] = useState(null);
  const controller = new AbortController();
  const signal = controller.signal;

  //When there have been new files queued, update the global store and trigger an upload
  useEffect(() => {
    const uploadFile = async (file) => {
      let formData = new FormData();
      formData.append("file", file);

      setCurrentUploadingFile(file.name);

      const res = await axios
        .post("/scan", formData, {
          signal,
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((res) => {
          setError(null);
        })
        .catch((err) => {
          throw err;
        });

      setCurrentUploadingFile(null);
      return res;
    };

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
          if (err.code !== "ERR_CANCELED") {
            setError(
              `Attempted upload for "${currentFile.name}" failed: ${err.message}`
            );
          }
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

    return () => {
      controller.abort();
    };
  }, [uploadQueue]);

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
    setError,
  ];
};

export default useUploadSVS;
