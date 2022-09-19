import { DataGrid, GridColDef, GridValueGetterParams } from "@mui/x-data-grid";

const columns: GridColDef[] = [
  { field: "filename", headerName: "Filename", width: 256 },
  { field: "tif", headerName: ".tif", width: 128 },
  { field: "png", headerName: ".png", width: 128 },
  { field: "mask", headerName: "Mask", width: 128 },
  {
    field: "dateCreated",
    headerName: "Date created",
    description: "This column has a value getter and is not sortable.",
    width: 192,
  }
];

const rows = [
  { id: 1, filename: "example1", tif: true, png: true, mask: true, dateCreated: "Tuesday" },
  { id: 2, filename: "example2", tif: true, png: true, mask: false, dateCreated: "Tuesday" },
  { id: 3, filename: "example3", tif: true, png: false, mask: true, dateCreated: "Tuesday" },
  { id: 4, filename: "example4", tif: true, png: false, mask: false, dateCreated: "Tuesday" },
  { id: 5, filename: "example5", tif: false, png: true, mask: true, dateCreated: "Tuesday" },
  { id: 6, filename: "example6", tif: false, png: true, mask: false, dateCreated: "Tuesday" },
  { id: 7, filename: "example7", tif: false, png: false, mask: true, dateCreated: "Tuesday" },
  { id: 8, filename: "example8", tif: false, png: false, mask: false, dateCreated: "Tuesday" },
];

const FileTable = () => {
  return (
    <div style={{ height: 400, width: "100%" }}>
      <DataGrid
        rows={rows}
        columns={columns}
        pageSize={100}
        rowsPerPageOptions={[5]}
        checkboxSelection
      />
    </div>
  );
};

export default FileTable;
