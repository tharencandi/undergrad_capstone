import axios from "axios";

const useServerAction = () => {
  const requestServerAction = async (ids, extension, action) => {
    let url = "";
    if (action === "delete") {
      await axios
        .delete("/scan", {
          params: {
            ids,
          },
        })
        .then((res) => {
          console.log(res);
        })
        .catch((err) => {
          console.log(err);
        });

      console.log(`Sent delete request with: `, ids);

      return;
    }

    if (action === "download") {
      url = "/scan";
    } else if (action === "generate") {
      url = "/scan/generate";
    }

    await axios
      .get(url, {
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

    console.log(`Sent ${action} request with: `, ids, extension);
  };

  return requestServerAction;
};

export default useServerAction;
