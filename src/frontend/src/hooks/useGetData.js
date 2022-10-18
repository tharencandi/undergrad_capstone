import axios from "axios";
import { useDispatch } from "react-redux";
import { setData } from "store/dataReducer";

const DUMMY_DATA = {
  123: {
    fileId: "123",
    fileName: "example1",
    tifStatus: "inProgress",
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
