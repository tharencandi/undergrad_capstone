import { useEffect } from "react";
import axios from "axios";

import { useSelector, useDispatch } from "react-redux";
import { setData } from "store/dataReducer";

const DUMMY_DATA = {
  123: {
    fileId: "123",
    fileName: "example1",
    created: "3rd December 2021",
    tifStatus: "none",
    pngStatus: "completed",
    maskStatus: "completed",
    downloadStatus: "none",
    uploadStatus: "none",
  },
  456: {
    fileId: "456",
    fileName: "example2",
    created: "2nd December 2021",
    tifStatus: "none",
    pngStatus: "completed",
    maskStatus: "completed",
    downloadStatus: "none",
    uploadStatus: "none",
  },
};

const useGetData = () => {
  const data = useSelector((state) => state.data);
  const dispatch = useDispatch();

  useEffect(() => {
    (async () => {
      // const res = await axios.get("/all");
      dispatch(setData(DUMMY_DATA));
    })();
  }, [dispatch]);

  return data;
};

export default useGetData;
