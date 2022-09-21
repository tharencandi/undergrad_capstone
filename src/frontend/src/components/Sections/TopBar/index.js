import ActionPanel from "./ActionPanel";
import InfoBox from "./InfoBox";

const TopBar = () => {
  return (
    <div className="flex flex-col-reverse h-[240px] gap-4 justify-center md:flex-row px-6 xl:px-12 xl:justify-between items-center md:h-[160px] lg:h-[130px] xl:h-[160px]">
      <ActionPanel></ActionPanel>
      <InfoBox></InfoBox>
    </div>
  );
};

export default TopBar;
