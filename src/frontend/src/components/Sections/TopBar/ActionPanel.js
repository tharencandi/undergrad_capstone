import Button from "components/UI/Button";

const ActionPanel = () => {
  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 justify-evenly gap-4 xl:gap-6">
      <div className="relative overflow-hidden inline-block md:mr-6 xl:mr-12 ">
        <Button variant="highlight">Upload SVS</Button>
        <input
          accept="image/*"
          multiple
          type="file"
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
        />
      </div>
      <Button>Download</Button>
      <Button>Generate</Button>
      <Button>Delete</Button>
    </div>
  );
};

export default ActionPanel;
