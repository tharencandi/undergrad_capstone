import { render, screen, act, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom";
import { Provider } from "react-redux";
import configureStore from "redux-mock-store";
import App from "../App";


describe("app", () => {
  const initialState = { selectedData: ["example"] };
  const mockStore = configureStore();
  let store;
  store = mockStore(initialState);

  const mockOverlayRoot = document.createElement("div");
  const mockBackdropRoot = document.createElement("div");
  mockOverlayRoot.setAttribute("id", "overlay-root");
  mockBackdropRoot.setAttribute("id", "backdrop-root");
  document.body.appendChild(mockOverlayRoot);
  document.body.appendChild(mockBackdropRoot);

  test("render app", async () => {
    await act( async () => {
        render(
            <Provider store={store}>
                <App />
            </Provider>
        );
    });
  });

  test("render app action bar", async () => {
    await act( async () => {
        render(
            <Provider store={store}>
                <App />
            </Provider>
        );
    });

    const uploadSvsBtn = screen.getByRole("button", { name: /upload svs/i });
    const downloadBtn = screen.getByRole("button", { name: /upload svs/i });
    const generateBtn = screen.getByRole("button", { name: /upload svs/i });
    const deleteBtn = screen.getByRole("button", { name: /upload svs/i });

    expect(uploadSvsBtn).toBeVisible();
    expect(downloadBtn).toBeVisible();
    expect(generateBtn).toBeVisible();
    expect(deleteBtn).toBeVisible();
  });

  test("render app helper text", async () => {
    await act( async () => {
        render(
            <Provider store={store}>
                <App />
            </Provider>
        );
    });

    const downloadTxt = screen.getByText(/ready for download/i);
    const processingTxt = screen.getByText(/being processed/i);
    const waitingTxt = screen.getByText(/waiting to be processed/i);

    expect(downloadTxt).toBeVisible();
    expect(processingTxt).toBeVisible();
    expect(waitingTxt).toBeVisible();
  });

  test("click generate and render prompt", async () => {
    await act( async () => {
        render(
            <Provider store={store}>
                <App />
            </Provider>
        );
    });

    const generateBtn = screen.getByRole("button", { name: /generate/i });
    fireEvent.click(generateBtn);

    const prompt = screen.getByText(/selected to generate/i);
    const confirmBtns = screen.getAllByRole("button", { name: /generate/i });
    const cancelBtn = screen.getByRole("button", { name: /cancel/i });

    // there should be two generate buttons on screen,
    // need to check for 2nd one
    expect(confirmBtns.length === 2).toBeTruthy();
    const confirmBtn = confirmBtns[0];

    expect(prompt).toBeVisible();
    expect(confirmBtn).toBeVisible();
    expect(cancelBtn).toBeVisible();
  });

  test("click delete and render prompt", async () => {
    await act( async () => {
        render(
            <Provider store={store}>
                <App />
            </Provider>
        );
    });

    const deleteBtn = screen.getByRole("button", { name: /delete/i });
    fireEvent.click(deleteBtn);

    const prompt = screen.getByText(/selected to delete/i);
    const confirmBtns = screen.getAllByRole("button", { name: /delete/i });
    const cancelBtn = screen.getByRole("button", { name: /cancel/i });

    // there should be two delete buttons on screen,
    // need to check for 2nd one
    expect(confirmBtns.length === 2).toBeTruthy();
    const confirmBtn = confirmBtns[0];

    expect(prompt).toBeVisible();
    expect(confirmBtn).toBeVisible();
    expect(cancelBtn).toBeVisible();
  });

  test("click generate and render prompt then cancel prompt", async () => {
    await act( async () => {
        render(
            <Provider store={store}>
                <App />
            </Provider>
        );
    });

    const generateBtn = screen.getByRole("button", { name: /generate/i });
    fireEvent.click(generateBtn);
    const cancelBtn = screen.getByRole("button", { name: /cancel/i });
    fireEvent.click(cancelBtn);

    // there should now only be one generate button on screen
    const generateBtns = screen.getAllByRole("button", { name: /generate/i });
    expect(generateBtns.length === 1).toBeTruthy();
  });

  test("click delete and render prompt then cancel prompt", async () => {
    await act( async () => {
        render(
            <Provider store={store}>
                <App />
            </Provider>
        );
    });

    const deleteBtn = screen.getByRole("button", { name: /delete/i });
    fireEvent.click(deleteBtn);
    const cancelBtn = screen.getByRole("button", { name: /cancel/i });
    fireEvent.click(cancelBtn);

    // there should now only be one delete button on screen
    const deleteBtns = screen.getAllByRole("button", { name: /delete/i });
    expect(deleteBtns.length === 1).toBeTruthy();
  });
});
