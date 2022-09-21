import ActionPanel from "./ActionPanel";
import InfoBox from "./InfoBox";

const TopBar = () => {
  return (
    <div className="flex px-12 justify-between items-center h-[160px]">
      <ActionPanel></ActionPanel>
      <InfoBox></InfoBox>
    </div>
  );
};

export default TopBar;
