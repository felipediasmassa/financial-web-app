import React, { useState } from "react";

import { DummyModel } from "../../models/dummyModel.model";

interface DummyComponent1Props {
  myFirstProp: string;
}

const DummyComponent2: React.FC<DummyComponent1Props> = () => {
  const [myDummyState, setMyDummyState] = useState<DummyModel[]>([]);

  return <div></div>;
};

export default DummyComponent2;
