import { useEffect, useState } from "react";

const useUploadSVS = () => {
  const [uploadQueue, setUploadQueue] = useState([]);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [currentUploadingFile, setCurrentUploadingFile] = useState(null);
  const [numberUploaded, setNumberUploaded] = useState(0);
  const [numberToUpload, setNumberToUpload] = useState(0);

  //When there have been new files queued, update the global store and trigger an upload
  useEffect(() => {
    console.log(uploadQueue);
    const uploadFile = async (file) => {
      setCurrentUploadingFile(file.name);

      // Dummy API call which waits for 1 second to resolve
      setUploadProgress(0);
      await new Promise((resolve) => setTimeout(resolve, 1000));
      setUploadProgress(20);
      await new Promise((resolve) => setTimeout(resolve, 1000));
      setUploadProgress(40);
      await new Promise((resolve) => setTimeout(resolve, 1000));
      setUploadProgress(60);
      await new Promise((resolve) => setTimeout(resolve, 1000));
      setUploadProgress(80);
      await new Promise((resolve) => setTimeout(resolve, 1000));
      setUploadProgress(100);

      setCurrentUploadingFile(null);
      return file.name;
    };

    // If there is already a file uploading, then do not start another upload
    if (currentUploadingFile) {
      return;
    }

    if (uploadQueue.length > 0) {
      const currentFile = uploadQueue[0];

      uploadFile(currentFile)
        .then((res) => {
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
    uploadQueue,
    (newFiles) => {
      setNumberToUpload((prevState) => prevState + newFiles.length);
      setUploadQueue((prevState) => [...prevState, ...newFiles]);
    },
    uploadProgress,
    currentUploadingFile,
    numberUploaded,
    numberToUpload,
  ];
};

export default useUploadSVS;
