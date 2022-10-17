import { createSlice } from "@reduxjs/toolkit";

const initialState = [];

// State handles the files which are selected on the client side
export const selectedDataSlice = createSlice({
  initialState,
  name: "selectedData",
  reducers: {
    setSelectedData: (state, action) => {
      state = action.payload;
      return state;
    },
  },
});

export const { setSelectedData } = selectedDataSlice.actions;

export default selectedDataSlice.reducer;
