import ReactDOM from "react-dom";
import Button from "components/UI/Button";
import React, { useState, useEffect } from "react";
import { Input } from "@mui/material";
import { useSelector } from "react-redux";
import axios from "axios";

const Backdrop = ({ modalController }) => {
  return (
    <div
      className="absolute inset-0 w-screen h-screen bg-black bg-opacity-70 flex justify-center items-center"
      onClick={() => {
        modalController(null);
      }}
    ></div>
  );
};

const Overlay = ({ cell, modalController }) => {
  const [newName, setNewName] = useState(cell.value);
  const [loading, setLoading] = useState(false);
  const [validName, setValidName] = useState(true);
  const [error, setError] = useState(null);

  const names = useSelector((state) => {
    console.log(state.data);
    return Object.keys(state.data).map((key) => {
      return state.data[key].fileName;
    });
  });

  useEffect(() => {
    if (
      (names.includes(newName) && newName !== cell.value) ||
      newName.length < 1
    ) {
      setValidName(false);
      return;
    }
    setValidName(true);
  }, [newName]);

  const submitHandler = async () => {
    setLoading(true);
    const params = { params: { ids: cell.id, new_name: newName } };

    axios
      .get("/name", params)
      .then((res) => {
        console.log(res);
        setError(null);
        modalController(null);
      })
      .catch((err) => {
        setError(err.message);
      });
    setLoading(false);
  };

  return (
    <div className="absolute inset-0 min-w-[400px] max-w-[500px] h-[300px] m-auto bg-white p-8 rounded-sm z-10 flex flex-col justify-between">
      <h2 className="subtitle1">Change name of file "{cell.value}":</h2>
      <div className="flex w-full flex-col h-[65px] gap-2">
        <Input
          value={newName}
          onChange={(e) => {
            setNewName(e.target.value);
          }}
        ></Input>
        {!validName && (
          <p className="warning text-body2">
            Another file already has the same name, please choose a different
            name
          </p>
        )}
        {error && <p className="warning text-body2">{error}</p>}
      </div>

      <div className="flex items-end justify-between">
        <Button
          onClick={() => {
            modalController(null);
          }}
          small={true}
        >
          Cancel
        </Button>
        {/* Submit Button */}
        <Button
          small={true}
          variant="highlight"
          disabled={loading || !validName ? true : false}
          onClick={submitHandler}
        >
          {loading ? "Saving..." : "Save"}
        </Button>
      </div>
    </div>
  );
};

// The variant is the delete, download or generate variant
const NameChangeNameChangeNameChangeNameChangeModal = ({
  cell,
  modalController,
}) => {
  return (
    <>
      {ReactDOM.createPortal(
        <Overlay cell={cell} modalController={modalController}></Overlay>,
        document.getElementById("overlay-root")
      )}
      {ReactDOM.createPortal(
        <Backdrop modalController={modalController}></Backdrop>,
        document.getElementById("backdrop-root")
      )}
    </>
  );
};

export default NameChangeNameChangeNameChangeNameChangeModal;
