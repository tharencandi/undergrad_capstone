import axios from "axios";

const useServerAction = () => {
  const requestServerAction = async (ids, extension, action, overwrite) => {
    let url = "";
    if (action === "delete") {
      await axios
        .delete("/scan", {
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

      console.log(`Sent delete request with: `, ids, extension);

      return;
    }

    let params = {};
    if (action === "download") {
      url = "/scan";
      params = { ids, extension };
    } else if (action === "generate") {
      url = "/scan/generate";
      params = { ids, extension, overwrite };
    }

    await axios
      .get(url, {
        params,
      })
      .then((res) => {
        console.log(res);
      })
      .catch((err) => {
        console.log(err);
      });

    console.log(`Sent ${action} request with: `, ids, extension);
  };

  return requestServerAction;
};

export default useServerAction;
