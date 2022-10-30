import { fireEvent, render, screen } from "@testing-library/react";
import OverwriteOption from "../OverwriteOption";

const mockSetChecked = jest.fn();

test("render overwrite option", () => {
    render(<OverwriteOption checked={[]}/>);
});

test("render overwrite option variant generate", () => {
    render(<OverwriteOption checked={[]} variant="generate"/>);
});

test("click overwrite option", () => {
    render(<OverwriteOption checked={[]} setChecked={mockSetChecked} variant=""/>);
    const overwriteOptions = screen.getAllByRole("checkbox");
    for (const overwriteOption of overwriteOptions) {
        fireEvent.click(overwriteOption);
    }
});

test("click overwrite option variant generate", () => {
    render(<OverwriteOption checked={[]} setChecked={mockSetChecked} variant="generate"/>);
    const overwriteOptions = screen.getAllByRole("checkbox");
    for (const overwriteOption of overwriteOptions) {
        fireEvent.click(overwriteOption);
    }
});

test("click and unclick overwrite option", () => {
    render(<OverwriteOption checked={[]} setChecked={mockSetChecked} variant=""/>);
    const overwriteOptions = screen.getAllByRole("checkbox");
    for (const overwriteOption of overwriteOptions) {
        fireEvent.click(overwriteOption);
    }

    for (const overwriteOption of overwriteOptions) {
        fireEvent.click(overwriteOption);
    }
});

test("click and unclick overwrite option variant generate", () => {
    render(<OverwriteOption checked={[]} setChecked={mockSetChecked} variant="generate"/>);
    const overwriteOptions = screen.getAllByRole("checkbox");
    for (const overwriteOption of overwriteOptions) {
        fireEvent.click(overwriteOption);
    }

    for (const overwriteOption of overwriteOptions) {
        fireEvent.click(overwriteOption);
    }
});
