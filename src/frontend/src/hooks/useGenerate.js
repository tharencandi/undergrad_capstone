import axios from "axios";

const useGenerate = () => {
  const requestGenerate = async (ids, extension) => {
    const res = await axios
      .get("/scan/generate", {
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

    console.log("Sent generate request with: ", ids, extension);
  };

  return requestGenerate;
};

export default useGenerate;
