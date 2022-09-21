import { useEffect, useState } from "react";
import axios from "axios";

const useGetData = () => {
  const [data, setData] = useState("");

  useEffect(() => {
    (async () => {
      const res = await axios.get("/all");
      setData(res.data);
    })();
  }, []);

  return data;
};

export default useGetData;
