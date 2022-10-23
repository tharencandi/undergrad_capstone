import { render, screen } from "@testing-library/react";
import "@testing-library/jest-dom";
import UploadModalContent from "../UploadModal";

describe("upload modal", () => {
  test("render upload modal", () => {
    const mockModalRoot = document.createElement("div");
    mockModalRoot.setAttribute("id", "upload-modal-root");
    document.body.appendChild(mockModalRoot)
  
    render(<UploadModalContent />);
  });
  
  test("render upload modal with upload progress", () => {
    const mockModalRoot = document.createElement("div");
    mockModalRoot.setAttribute("id", "upload-modal-root");
    document.body.appendChild(mockModalRoot)
  
    const numberUploaded = 2;
    const numberToUpload = 3;
    render(<UploadModalContent numberUploaded={numberUploaded} numberToUpload={numberToUpload}/>);
  
    const statusMessage = screen.getByText(/Uploaded 2 out of 3./i);
    expect(statusMessage).toBeVisible();
  });
  
  test("render upload modal with currently upload file", () => {
    const mockModalRoot = document.createElement("div");
    mockModalRoot.setAttribute("id", "upload-modal-root");
    document.body.appendChild(mockModalRoot)
  
    render(<UploadModalContent currentUploadingFile={"arbitrary file.txt"}/>);
  
    const statusMessage = screen.getByText(/Currently uploading: arbitrary file.txt/i);
    expect(statusMessage).toBeVisible();
  });
});
