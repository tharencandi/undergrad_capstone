import axios from "axios";
import { useSelector } from "react-redux";

const useServerAction = () => {
  const data = useSelector((state) => {
    return state.data;
  });

  const requestServerAction = async (ids, extension, action, overwrite) => {
    ids = ids.map((id) => data[id].fileName);
    // Clean extensions
    extension = extension.map((ext) => {
      if (ext[0] === ".") {
        return ext.slice(1);
      }
      return ext;
    });

    // Convert the list of ids to list of names

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
      url = "/generate";
      params = { ids, extension, overwrite };
      await axios
      .post(url,
        params
      )
      .then((res) => {
        console.log(res);
      })
      .catch((err) => {
        console.log(err);
      });

      console.log(`Sent ${action} request with: `, ids, extension);
      return
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
