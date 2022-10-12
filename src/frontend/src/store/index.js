import { configureStore } from "@reduxjs/toolkit";
import dataReducer from "./dataReducer";
import uploadQueueReducer from "./uploadQueueReducer";

export const store = configureStore({
  reducer: {
    data: dataReducer,
    uploadQueue: uploadQueueReducer,
  },
});
