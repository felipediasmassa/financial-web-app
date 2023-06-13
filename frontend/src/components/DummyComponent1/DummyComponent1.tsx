import React, { useState } from "react";

import { DummyModel } from "../../models/dummyModel.model";

interface DummyComponent1Props {
  myFirstProp: string;
}

const DummyComponent1: React.FC<DummyComponent1Props> = () => {
  const [myDummyState, setMyDummyState] = useState<DummyModel[]>([]);

  return <div></div>;
};

export default DummyComponent1;
