import axios from "axios";
import { useSelector } from "react-redux";

const useServerAction = () => {
  const data = useSelector((state) => state.data);
  const requestServerAction = async (
    ids,
    extension,
    action,
    overwrite = false
  ) => {
    // // Test error generation - comment out
    // throw new Error("Error performing specified request: Error code 1234");

    // Clean extensions
    extension = extension.map((ext) => {
      if (ext[0] === ".") {
        return ext.slice(1);
      }
      return ext;
    });

    // Convert the list of ids to list of names
    ids = ids.map((id) => data[id].fileName);

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
      return;
    }

    if (action === "download") {
      await axios({
        url: "/scan",
        method: "GET",
        responseType: "blob",
        params: { ids, extension },
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
          return response;
        })
        .catch((err) => {
          throw new Error(err.message);
        });
      return;
    }

    if (action === "generate") {
      const url = "/generate";
      const params = { ids, extension, overwrite };
      await axios
        .post(url, params)
        .then((res) => {
          return res;
        })
        .catch((err) => {
          throw new Error(err.message);
        });
      return;
    }

    throw new Error("Unknown request type");
  };

  return requestServerAction;
};

export default useServerAction;
