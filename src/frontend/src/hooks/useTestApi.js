import { useEffect, useState } from "react";
import axios from "axios";

const useTestApi = () => {
  const [data, setData] = useState("");

  useEffect(() => {
    (async () => {
      const res = await axios.get("/hi");
      setData(res.data);
    })();
  });

  return data;
};

export default useTestApi;
