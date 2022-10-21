import axios from "axios";
import { useDispatch } from "react-redux";
import { setData } from "store/dataReducer";

const DUMMY_DATA = {
  123: {
    fileId: "123",
    fileName: "example1.svs",
    tifStatus: "inProgress",
    pngStatus: "none",
    maskStatus: "completed",
    created: "2nd December 2021",
    downloadProgress: "none",
  },
  456: {
    fileId: "456",
    fileName: "example2.svs",
    tifStatus: "completed",
    pngStatus: "none",
    maskStatus: "completed",
    created: "2nd December 2021",
    downloadProgress: "none",
  },
  12345: {
    fileId: "12345",
    fileName: "example3.svs",
    tifStatus: "pending",
    pngStatus: "none",
    maskStatus: "completed",
    created: "2nd December 2021",
    downloadProgress: "none",
  },
  1234: {
    fileId: "1234",
    fileName: "example4.svs",
    tifStatus: "pending",
    pngStatus: "none",
    maskStatus: "completed",
    created: "2nd December 2021",
    downloadProgress: "none",
  },
  2234: {
    fileId: "2234",
    fileName: "example5.svs",
    tifStatus: "pending",
    pngStatus: "none",
    maskStatus: "completed",
    created: "2nd December 2021",
    downloadProgress: "none",
  },
};
const useGetData = () => {
  const dispatch = useDispatch();

  const fetchData = async () => {
    console.log("Refreshing data....");
    dispatch(setData(DUMMY_DATA));
    // await axios
    //   .get("/all")
    //   .then((res) => {
    //     dispatch(setData(res.data));
    //   })
    //   .catch((err) => {
    //     console.error(err);
    //   });
  };

  return fetchData;
};

export default useGetData;
