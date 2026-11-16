import SceneRender, { type RenderId } from "./scene-render";

const stages: RenderId[] = ["chip", "wafer", "lithography", "package"];

/** Conceptual studio renders, without manufacturer or process-accuracy claims. */
export default function SiliconScene({ stage = 0 }: { stage?: number }) {
  return <SceneRender id={stages[stage] || "chip"} className={`silicon-scene scene-${stage}`} sizes="(max-width: 760px) 100vw, 650px" eager/>;
}
