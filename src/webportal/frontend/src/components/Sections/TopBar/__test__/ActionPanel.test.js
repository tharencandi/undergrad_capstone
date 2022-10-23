import { render, screen } from "@testing-library/react";
import ActionPanel from "../ActionPanel";
import { Provider } from "react-redux";
import configureStore from 'redux-mock-store';

describe("with react testing library", () => {
    const initialState = { selectedData: [] };
    const mockStore = configureStore();
    let store;

    test("render action panel", () => {
        store = mockStore(initialState);

        render(
            <Provider store={store}>
                <ActionPanel />
            </Provider>
        );
    });
});
