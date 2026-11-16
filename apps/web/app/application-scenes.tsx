import SceneRender from "./scene-render";
import type { ApplicationSceneId } from "./research-types";

/** Generated studio illustrations; interactive callouts are separate accessible controls. */
export function ApplicationObject({ scene, eager = false, thumbnail = false }: { scene: ApplicationSceneId; eager?: boolean; thumbnail?: boolean }) {
  return <SceneRender id={scene} eager={eager} className={`application-object object-${scene}`} sizes={thumbnail ? "(max-width: 600px) 100vw, (max-width: 900px) 33vw, 400px" : "(max-width: 900px) 100vw, 900px"}/>;
}
