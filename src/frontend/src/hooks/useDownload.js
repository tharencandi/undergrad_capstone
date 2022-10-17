import axios from "axios";

const useDownload = () => {
  const requestDownload = async (ids, extension) => {
    const res = await axios
      .get("/scan", {
        params: {
          ids,
          extension,
        },
      })
      .then((res) => {
        console.log(res);
      })
      .catch((err) => {
        console.log(err);
      });

    console.log("Sent download request with: ", ids, extension);
  };

  return requestDownload;
};

export default useDownload;
