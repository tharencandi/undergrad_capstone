import { render, screen } from "@testing-library/react";
import OverwriteOption from "../OverwriteOption";

test("render overwrite option", () => {
    render(<OverwriteOption checked={["example"]} setChecked={["example"]}/>);
});
