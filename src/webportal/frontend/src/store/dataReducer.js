import { createSlice } from "@reduxjs/toolkit";

const initialState = {};

export const dataSlice = createSlice({
  initialState,
  name: "data",
  reducers: {
    setData: (state, action) => {
      state = action.payload;
      return state;
    },
  },
});

export const { setData } = dataSlice.actions;

export default dataSlice.reducer;
