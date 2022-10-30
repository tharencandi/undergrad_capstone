import { fireEvent, render, screen } from "@testing-library/react";
import CheckList from "../CheckList";

const mockSetChecked = jest.fn();

test("render checklist", () => {
    render(<CheckList checked={[]}/>);
});

test("render checklist variant generate", () => {
    render(<CheckList checked={[]} variant="generate"/>);
});

test("click checklist", () => {
    render(<CheckList checked={[]} setChecked={mockSetChecked} variant=""/>);
    const checkLists = screen.getAllByRole("checkbox");
    for (const checkList of checkLists) {
        fireEvent.click(checkList);
    }
});

test("click checklist variant generate", () => {
    render(<CheckList checked={[]} setChecked={mockSetChecked} variant="generate"/>);
    const checkLists = screen.getAllByRole("checkbox");
    for (const checkList of checkLists) {
        fireEvent.click(checkList);
    }
});

test("click and unclick checklist", () => {
    render(<CheckList checked={[]} setChecked={mockSetChecked} variant=""/>);
    const checkLists = screen.getAllByRole("checkbox");
    for (const checkList of checkLists) {
        fireEvent.click(checkList);
    }

    for (const checkList of checkLists) {
        fireEvent.click(checkList);
    }
});

test("click and unclick checklist variant generate", () => {
    render(<CheckList checked={[]} setChecked={mockSetChecked} variant="generate"/>);
    const checkLists = screen.getAllByRole("checkbox");
    for (const checkList of checkLists) {
        fireEvent.click(checkList);
    }

    for (const checkList of checkLists) {
        fireEvent.click(checkList);
    }
});
