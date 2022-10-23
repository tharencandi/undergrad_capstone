import { render, screen } from "@testing-library/react";
import InfoBox from "../index";
import InfoBoxCell from "../InfoBoxCell";

test("render info box", () => {
    render(<InfoBox />);
});
