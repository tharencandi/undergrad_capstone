import { render, screen } from "@testing-library/react";
import CheckList from "../CheckList";

test("render checklist", () => {
    render(<CheckList checked={[]}/>);
});
