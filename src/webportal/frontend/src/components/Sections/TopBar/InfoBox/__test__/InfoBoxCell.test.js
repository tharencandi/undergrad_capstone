import { render, screen } from "@testing-library/react";
import "@testing-library/jest-dom";
import InfoBoxCell from "../InfoBoxCell";

describe("info box cell", () => {
    test("render empty info box", () => {
        render(<InfoBoxCell />);
    });
    
    test("render info box with text input", () => {
        const testInfoBoxText = "arbitrary text";
        render(<InfoBoxCell text={testInfoBoxText}/>);
        const infoBoxText = screen.getByText(testInfoBoxText);
    
        expect(infoBoxText).toBeVisible();
    });
    
    test("render info box with icon input", () => {
        const testInfoBoxIcon = "arbitrary icon";
        render(<InfoBoxCell icon={testInfoBoxIcon}/>);
        const infoBoxIcon = screen.getByText(testInfoBoxIcon);
    
        expect(infoBoxIcon).toBeVisible();
    });
});
