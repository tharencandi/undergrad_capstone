import { useEffect } from "react";
import axios from "axios";

import { useDispatch } from "react-redux";
import { setData } from "store/dataReducer";

const useGetData = () => {
  const dispatch = useDispatch();

  useEffect(() => {
    (async () => {
      const res = await axios.get("/all");
      dispatch(setData(res.data));
    })();
  }, [dispatch]);
};

export default useGetData;
