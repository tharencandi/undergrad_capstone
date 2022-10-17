import { configureStore } from "@reduxjs/toolkit";
import dataReducer from "./dataReducer";
import selectedDataReducer from "./selectedDataReducer";

export const store = configureStore({
  reducer: {
    data: dataReducer,
    selectedData: selectedDataReducer,
  },
});
