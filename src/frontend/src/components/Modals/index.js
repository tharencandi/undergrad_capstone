import ReactDOM from "react-dom";
import CheckboxList from "./CheckList";
import Button from "components/UI/Button";
import React from "react";
import { useSelector } from "react-redux";
import useServerAction from "hooks/useServerAction";

const Backdrop = ({ modalController }) => {
  return (
    <div
      className="absolute inset-0 w-screen h-screen bg-black bg-opacity-70 flex justify-center items-center"
      onClick={() => {
        modalController("none");
      }}
    ></div>
  );
};

const Overlay = ({ variant, modalController }) => {
  const [checked, setChecked] = React.useState([]);
  const selectedData = useSelector((state) => state.selectedData);
  const requestServerAction = useServerAction();

  return (
    <div className="absolute inset-0 min-w-[400px] max-w-[750px] h-[500px] m-auto bg-white p-8 rounded-sm z-10 flex flex-col">
      <h2 className="subtitle1">
        {selectedData.length} file/s selected to {variant}:
      </h2>
      <CheckboxList checked={checked} setChecked={setChecked}></CheckboxList>
      <div className="flex-grow flex items-end justify-between">
        <Button
          onClick={() => {
            modalController("none");
          }}
        >
          Cancel
        </Button>
        {/* Submit Button */}
        <Button
          variant="highlight"
          onClick={() => {
            requestServerAction(selectedData, checked, variant);
          }}
        >
          {variant[0].toUpperCase() + variant.substring(1)}
        </Button>
      </div>
    </div>
  );
};

// The variant is the download or generate variant
const Modal = ({ variant, modalController }) => {
  return (
    <>
      {ReactDOM.createPortal(
        <Overlay variant={variant} modalController={modalController}></Overlay>,
        document.getElementById("overlay-root")
      )}
      {ReactDOM.createPortal(
        <Backdrop modalController={modalController}></Backdrop>,
        document.getElementById("backdrop-root")
      )}
    </>
  );
};

export default Modal;
