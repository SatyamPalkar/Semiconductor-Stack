# Studio 3D visual rework — 16 November 2026

The complete application illustration set has been replaced with detailed studio renders. The nine scenes cover AI servers, an electric vehicle, urban infrastructure, industrial robotics, aviation, engineering design, energy, medical equipment and connected devices. Four additional renders cover the silicon die, wafer, generic precision-processing equipment and conceptual packaging. The homepage silicon core uses the same die artwork.

The visual direction uses realistic curved geometry, recognizable proportions, finely detailed glass/metal/polymer materials, soft white key lighting, restrained accent rims and near-black studio backgrounds. These are AI-generated raster illustrations in a 3D rendering style; they are not rotatable meshes, real product photographs, verified component diagrams or financial evidence. Existing source-backed explanations, company examples and financial boundaries remain intact.

## Assets and prompts

- Generated with the **built-in `image_gen` tool**; no CLI/API fallback or hosted-model evaluation was used.
- All final assets are in [`apps/web/public/visuals/3d`](../apps/web/public/visuals/3d/). Thirteen scenes each have 768px and 1536px WebP versions: **26 files, 2,786,144 bytes total**.
- [`data/catalog/visual-assets.json`](../data/catalog/visual-assets.json) preserves the complete final prompt set, tool provenance, generation date, output dimensions and paths. Source PNG copies and browser review captures stay in ignored `data/interim` directories.
- The car brief explicitly requires realistic vehicle proportions, curved silver bodywork, glazing, a charging connection and a visible underfloor battery. The other scene prompts specify the subject, detailed materials, camera composition, lighting, conceptual scope and absence of branding/annotations.

## Interface changes

`scene-render.tsx` serves local responsive assets through native picture sources and the static-export-compatible Next Image component. `application-scenes.tsx` and `story-graphics.tsx` now select those renders. The business and application pages share the visual style without new packages or a WebGL dependency.

Scene callouts use the same exact 3:2 image frame, separate 44px-or-larger accessible buttons and smaller visible number pins. Each selection updates the task strip, figure footer and existing explanation. Callout locations are explicitly illustrative. Full-bleed previews carry the same artwork into the homepage story cards. Source scope and AI-generation labels remain visible; motion respects reduced-motion preferences.

## Executed verification

- TypeScript and Next static production builds passed.
- The new responsive render workflow passed, covering all nine scenes at 1440/768/393/320px, local responsive-image loading, minimum control sizes, non-overlapping touch areas, keyboard activation, matching task captions and no page overflow. It also verifies loading of all four business renders.
- Final complete browser run: **32/32 workflows passed** against the production export, including all existing research workflows and the new studio-render checks.
- All thirteen generated source images were visually inspected. Integrated desktop captures of the car, AI racks, infrastructure, robot and homepage, plus the phone car capture, were inspected. Further captures remain local in ignored `data/interim/web-review`.
- Backend tests were not rerun for this presentation-only change. No cloud deployment or GitHub push was performed in this rework.

## Review locally

- [Electric vehicle](http://127.0.0.1:3100/applications/?world=electric-mobility)
- [All nine application worlds](http://127.0.0.1:3100/applications/)
- [Homepage and business story](http://127.0.0.1:3100/)

The retained static preview is PID 54834 on port 3100. Stop it with `kill 54834`; restart with `make preview`. The existing API is PID 77927 on port 8100; stop with `kill 77927` and restart with `make api`.
