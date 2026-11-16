import Image from "next/image";

export type RenderId = "ai" | "car" | "city" | "robot" | "plane" | "design" | "energy" | "health" | "connected" | "chip" | "wafer" | "lithography" | "package";

const descriptions: Record<RenderId, string> = {
  ai: "3D render of AI server racks with an accelerator tray, network cabling and power connections",
  car: "3D render of an electric car with curved silver bodywork, a visible underfloor battery and charging connection",
  city: "3D render of glass office buildings, a landscaped urban district and a cable-stayed bridge",
  robot: "3D render of a detailed industrial robot arm and gripper above a machined part",
  plane: "3D render of a twin-engine passenger aircraft with curved fuselage, wings and cockpit",
  design: "3D render of an engineering workstation displaying a turbine model and sectional view",
  energy: "3D render of a wind turbine, solar panels and an energy storage cabinet",
  health: "3D render of a patient monitor, measurement accessories and medical cart",
  connected: "3D render of a smartphone, smartwatch, wireless router and earbuds",
  chip: "3D render of an intricate iridescent silicon die on a circuit substrate",
  wafer: "3D render of an iridescent silicon wafer with an array of chip dies",
  lithography: "3D render of generic precision-processing equipment above a silicon wafer",
  package: "3D render of a conceptual exploded semiconductor package with chiplets and connections",
};

/** Local responsive rasters. Illustrative artwork, never product or financial evidence. */
export default function SceneRender({ id, className = "", eager = false, sizes = "(max-width: 900px) 100vw, 900px" }: { id: RenderId; className?: string; eager?: boolean; sizes?: string }) {
  return <picture className={`scene-render ${className}`} data-scene={id}>
    <source type="image/webp" srcSet={`/visuals/3d/${id}-768.webp 768w, /visuals/3d/${id}-1536.webp 1536w`} sizes={sizes}/>
    <Image src={`/visuals/3d/${id}-1536.webp`} width={1536} height={1024} alt={descriptions[id]} unoptimized loading={eager ? "eager" : "lazy"} decoding="async"/>
  </picture>;
}
