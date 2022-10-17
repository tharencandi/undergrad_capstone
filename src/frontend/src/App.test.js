import { render, fireEvent, screen } from "@testing-library/react";
import App from "./App";

test("renders action bar", () => {
    render(<App />);
    const uploadSvsBtn = screen.getByText("Upload SVS");
    const downloadBtn = screen.getByText("Download");
    const generateBtn = screen.getByText("Generate");
    const deleteBtn = screen.getByText("Delete");

    expect(uploadSvsBtn).toBeInTheDocument();
    expect(downloadBtn).toBeInTheDocument();
    expect(generateBtn).toBeInTheDocument();
    expect(deleteBtn).toBeInTheDocument();
});

test("renders helper text", () => {
    render(<App />);
    const downloadText = screen.getByText("Ready for download");
    const processingText = screen.getByText("Being processed");
    const waitingText = screen.getByText("Waiting to be processed");

    expect(downloadText).toBeInTheDocument();
    expect(processingText).toBeInTheDocument();
    expect(waitingText).toBeInTheDocument();
});

test("download click and render prompt", () => {
    render(<App />);
    const downloadBtn = screen.getByText("Download");

    fireEvent.click(downloadBtn);

    const downloadPrompt = screen.getByText(/files selected to download/i)
    const cancelBtn = screen.getByText("Cancel");
    const downloadBtn = screen.getByText("Generate");

    expect(downloadPrompt).toBeInTheDocument();
    expect(cancelBtn).toBeInTheDocument();
    expect(downloadBtn).toBeInTheDocument();
});

test("generate click and render prompt", () => {
    render(<App />);
    const generateBtn = screen.getByText("Generate");

    fireEvent.click(generateBtn);

    const generatePrompt = screen.getByText(/files selected to generate/i)
    const cancelBtn = screen.getByText("Cancel");
    const generateBtn = screen.getByText("Generate");

    expect(generatePrompt).toBeInTheDocument();
    expect(cancelBtn).toBeInTheDocument();
    expect(generateBtn).toBeInTheDocument();
});
