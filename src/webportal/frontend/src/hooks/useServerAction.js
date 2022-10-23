import axios from "axios";
import { act } from "react-dom/test-utils";
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
          return res;
        })
        .catch((err) => {
          throw new Error(err.message);
        });

      console.log(`Sent delete request with: `, ids, extension);

      return;
    }

    let params = {};
    if (action === "download") {
      url = "/scan";
      params = { ids, extension };

      await axios({
        url,
        method: "GET",
        responseType: "blob",
        params, // important
      })
        .then((response) => {
          // Simulate error - comment out later
          // throw new Error("Failed to download file: Error code 1234");

          // create file link in browser's memory
          const href = URL.createObjectURL(response.data);

          // create "a" HTML element with href to file & click
          const link = document.createElement("a");
          link.href = href;
          link.setAttribute("download", `${ids}.${extension}`); //or any other extension
          document.body.appendChild(link);
          link.click();

          // clean up "a" element & remove ObjectURL
          document.body.removeChild(link);
          URL.revokeObjectURL(href);
        })
        .catch((err) => {
          throw new Error(err.message);
        });
      return;
    } else if (action === "generate") {
      url = "/generate";
      params = { ids, extension, overwrite };
      await axios
        .post(url, params)
        .then((res) => {
          console.log(res);
        })
        .catch((err) => {
          console.log(err);
        });

      console.log(`Sent ${action} request with: `, ids, extension);

      await axios
        .get(url, {
          params: params,
        })
        .then((res) => {
          console.log(res);
        })
        .catch((err) => {
          console.log(err);
        });
      return;
    }

    console.log("Unknown server request type: ", action);
  };

  return requestServerAction;
};

export default useServerAction;
