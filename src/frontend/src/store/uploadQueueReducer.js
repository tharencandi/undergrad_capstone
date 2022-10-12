import { createSlice } from "@reduxjs/toolkit";

const initialState = {};

// State handles the files which are pending upload on the client side only. File is moved out of here when an upload is initialised.
export const uploadQueueSlice = createSlice({
  initialState,
  name: "uploadQueue",
  reducers: {
    setUploadQueue: (state, action) => {
      state = action.payload;
      return state;
    },
  },
});

export const { setData } = uploadQueueSlice.actions;

export default uploadQueueSlice.reducer;
