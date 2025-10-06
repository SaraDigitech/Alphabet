import { configureStore } from "@reduxjs/toolkit";
import { api } from "./slices/api";

export const store = configureStore({
  reducer: {
    [api.reducerPath]: api.reducer,
  },
  middleware: (getDefault) => getDefault().concat(api.middleware),
});


