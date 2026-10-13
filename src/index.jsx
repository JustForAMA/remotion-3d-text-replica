import { registerRoot, Composition } from "remotion";
import { Text3D } from "./Text3D.jsx";
const Root = () => <Composition id="Text3D" component={Text3D} durationInFrames={180} fps={30} width={1920} height={1080} />;
registerRoot(Root);
