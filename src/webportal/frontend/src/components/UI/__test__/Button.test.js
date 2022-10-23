import { render, screen } from "@testing-library/react";
import "@testing-library/jest-dom";
import Button from "../Button";

describe("button", () => {
    test("render button", () => {
        render(<Button/>);
        const button = screen.getByRole("button");

        expect(button).toBeVisible();
    });
    
    test("render button as disabled", () => {
        render(<Button disabled={true}/>);
        const button = screen.getByRole("button");

        expect(button).toBeVisible();
        expect(button.classList.contains("opacity-50")).toBeTruthy();
    });

    test("render button as danger", () => {
        render(<Button danger={true}/>);
        const button = screen.getByRole("button");

        expect(button).toBeVisible();
        expect(button.classList.contains("bg-red")).toBeTruthy();
    });

    test("render button as highlight", () => {
        render(<Button highlight={true}/>);
        const button = screen.getByRole("button");

        expect(button).toBeVisible();
        expect(button.classList.contains("bg-primary")).toBeTruthy();
    });

    test("render button as not highlight", () => {
        render(<Button highlight={false}/>);
        const button = screen.getByRole("button");

        expect(button).toBeVisible();
        expect(button.classList.contains("bg-secondary")).toBeTruthy();
    });
});
