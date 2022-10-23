import { render, screen, act } from "@testing-library/react";
import FileTable from "../index";
import { Provider } from "react-redux";
import configureStore from 'redux-mock-store';

describe("with react testing library", () => {
    const initialState = {};
    const mockStore = configureStore();
    let store;

    test("render file table", async () => {
        store = mockStore(initialState);

        await act( async () => {
            render(
                <Provider store={store}>
                    <FileTable />
                </Provider>
            );
        });
    });
});
