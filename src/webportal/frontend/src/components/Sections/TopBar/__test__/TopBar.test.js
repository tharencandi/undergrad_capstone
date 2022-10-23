import { render, screen } from "@testing-library/react";
import TopBar from "../index";
import { Provider } from "react-redux";
import configureStore from 'redux-mock-store';

describe("with react testing library", () => {
    const initialState = { selectedData: [] };
    const mockStore = configureStore();
    let store;

    test("render top bar", () => {
        store = mockStore(initialState);

        render(
            <Provider store={store}>
                <TopBar />
            </Provider>
        );
    });
});
