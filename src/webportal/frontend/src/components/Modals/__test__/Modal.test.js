import { render, screen } from "@testing-library/react";
import "@testing-library/jest-dom";
import { Provider } from "react-redux";
import configureStore from "redux-mock-store";
import Modal from "../index";

describe("modal", () => {
  const mockModalController = jest.fn();
  const mockOverlayRoot = document.createElement("div");
  const mockBackdropRoot = document.createElement("div");
  mockOverlayRoot.setAttribute("id", "overlay-root");
  mockBackdropRoot.setAttribute("id", "backdrop-root");
  document.body.appendChild(mockOverlayRoot);
  document.body.appendChild(mockBackdropRoot);

  const initialState = { selectedData: [""], checked: [""], setChecked: [""], overwrite: [""], setOverwrite: [""] };
  const mockStore = configureStore();
  let store;
  store = mockStore(initialState);

  test("render delete modal", () => {
    render(
      <Provider store={store}>
        <Modal variant="delete" modalController={mockModalController}/>
      </Provider>
    );

    const prompt = screen.getByText(/selected to delete/i);
    const button = screen.getByRole("button", { name: /delete/i });
    const cancelButton = screen.getByRole("button", { name: /cancel/i });

    expect(prompt).toBeVisible();
    expect(button).toBeVisible();
    expect(cancelButton).toBeVisible();
  });

  test("render download modal", () => {
    render(
      <Provider store={store}>
        <Modal variant="download" modalController={mockModalController}/>
      </Provider>
    );

    const prompt = screen.getByText(/selected to download/i);
    const button = screen.getByRole("button", { name: /download/i });
    const cancelButton = screen.getByRole("button", { name: /cancel/i });

    expect(prompt).toBeVisible();
    expect(button).toBeVisible();
    expect(cancelButton).toBeVisible();
  });

  test("render generate modal", () => {
    render(
      <Provider store={store}>
        <Modal variant="generate" modalController={mockModalController}/>
      </Provider>
    );

    const prompt = screen.getByText(/selected to generate/i);
    const button = screen.getByRole("button", { name: /generate/i });
    const cancelButton = screen.getByRole("button", { name: /cancel/i });

    expect(prompt).toBeVisible();
    expect(button).toBeVisible();
    expect(cancelButton).toBeVisible();
  });
});
