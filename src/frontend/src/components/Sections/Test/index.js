import useTestApi from "hooks/useTestApi";

const Test = () => {
  const data = useTestApi();

  return <div>API test data: {data}</div>;
};

export default Test;
