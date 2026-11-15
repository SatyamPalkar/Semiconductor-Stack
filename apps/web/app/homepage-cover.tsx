"use client";

import Link from "next/link";
import { useId, useState, type CSSProperties } from "react";
import { ArrowDown, ArrowUpRight, Building2, CarFront, Cpu, MoveUpRight, Plane, Bot, Zap } from "lucide-react";
import type { Snapshot } from "./research-types";
import styles from "./homepage-cover.module.css";

const worlds = [
  { id: "ai-cloud", label: "AI & cloud", detail: "Intelligence at scale", icon: Cpu, color: "#a1b6ff", x: 49, y: 12 },
  { id: "electric-mobility", label: "Electric mobility", detail: "A new kind of drive", icon: CarFront, color: "#8aebc3", x: 82, y: 33 },
  { id: "smart-infrastructure", label: "Cities & buildings", detail: "Infrastructure that senses", icon: Building2, color: "#edc786", x: 79, y: 72 },
  { id: "automation", label: "Automation", detail: "Precision in motion", icon: Bot, color: "#a3c7ff", x: 46, y: 89 },
  { id: "energy", label: "Energy", detail: "Power, intelligently managed", icon: Zap, color: "#edaaa6", x: 15, y: 67 },
  { id: "aviation", label: "Aviation", detail: "Control above the clouds", icon: Plane, color: "#c7adf6", x: 18, y: 29 },
];

/** Decorative orbital connections express shared chip functions, never supplier routes. */
function SiliconUniverse() {
  const prefix = useId().replaceAll(":", "");
  const [active, setActive] = useState<number | null>(null);
  const selected = active === null ? null : worlds[active];
  return <div className={styles.universe} style={{ "--active-color": selected?.color || "#a7a4ff" } as CSSProperties}>
    <svg viewBox="0 0 600 600" className={styles.universeArt} aria-hidden="true">
      <defs>
        <radialGradient id={`${prefix}-aura`}><stop stopColor="#8882ff" stopOpacity=".2"/><stop offset=".5" stopColor="#5758cd" stopOpacity=".09"/><stop offset="1" stopColor="#5758cd" stopOpacity="0"/></radialGradient>
        <linearGradient id={`${prefix}-base`} x1="0" y1="0" x2=".8" y2="1"><stop stopColor="#45516b"/><stop offset=".45" stopColor="#20283c"/><stop offset="1" stopColor="#111726"/></linearGradient>
        <linearGradient id={`${prefix}-die`} x1="0" y1="0" x2="1" y2="1"><stop stopColor="#b8b3ff"/><stop offset=".36" stopColor="#7479db"/><stop offset=".7" stopColor="#393a83"/><stop offset="1" stopColor="#22274e"/></linearGradient>
        <linearGradient id={`${prefix}-edge`} x1="0" y1="0" x2="1" y2="1"><stop stopColor="#c6c6ff"/><stop offset=".5" stopColor="#777fc4"/><stop offset="1" stopColor="#333d69"/></linearGradient>
        <linearGradient id={`${prefix}-trace`} x1="0" x2="1"><stop stopColor="#83f4bc" stopOpacity="0"/><stop offset=".5" stopColor="#b4c6ff"/><stop offset="1" stopColor="#b4c6ff" stopOpacity="0"/></linearGradient>
        <filter id={`${prefix}-shadow`} x="-50%" y="-50%" width="200%" height="220%"><feDropShadow dx="0" dy="22" stdDeviation="18" floodColor="#000" floodOpacity=".65"/></filter>
      </defs>
      <circle cx="300" cy="298" r="280" fill={`url(#${prefix}-aura)`}/>
      <g className={styles.orbits} fill="none" stroke="#9caed2">
        <circle cx="300" cy="300" r="237" strokeOpacity=".12" strokeDasharray="1 7"/>
        <circle cx="300" cy="300" r="184" strokeOpacity=".13"/>
        <circle cx="300" cy="300" r="139" strokeOpacity=".12" strokeDasharray="2 9"/>
        <ellipse cx="300" cy="300" rx="267" ry="104" transform="rotate(-33 300 300)" strokeOpacity=".12"/>
      </g>
      <g fill="none" stroke={`url(#${prefix}-trace)`} strokeWidth="1">
        <path d="M300 72V191M491 198L389 256M474 432L387 348M276 534V392M90 402L209 338M108 174L213 247" opacity=".35"/>
        <path className={styles.signal} d="M300 72V191M491 198L389 256M474 432L387 348M276 534V392M90 402L209 338M108 174L213 247" strokeDasharray="3 24"/>
      </g>
      <g fill="#afb8e4"><circle cx="196" cy="88" r="2"/><circle cx="528" cy="354" r="2"/><circle cx="170" cy="496" r="2"/><circle cx="436" cy="140" r="2"/><circle cx="103" cy="305" r="2"/></g>
      <g className={styles.chip} filter={`url(#${prefix}-shadow)`}>
        <path d="M300 196L416 260V331L300 397L184 331V260Z" fill="#111726" stroke="#465074"/>
        <path d="M184 260L300 325L416 260V277L300 343L184 277Z" fill="#29354b" stroke="#586589" strokeWidth=".7"/>
        <path d="M300 183L416 249L300 316L184 249Z" fill={`url(#${prefix}-base)`} stroke="#7c89a8" strokeWidth="1.2"/>
        <g fill="none" stroke="#a9b69f" strokeWidth="1.4" opacity=".8">{Array.from({length:9}, (_,i)=><g key={i}>
          <path d={`M${206+i*10} ${239-i*5.6}l-11 -6M${320+i*10} ${294-i*5.7}l11 6M${204+i*10} ${261+i*5.7}l-10 6M${320+i*10} ${196+i*5.7}l11 -6`}/>
        </g>)}</g>
        <path d="M300 207L374 249V271L300 314L226 271V249Z" fill="#343d72" stroke="#8b96d4"/>
        <path d="M300 203L375 246L300 290L225 246Z" fill={`url(#${prefix}-die)`} stroke={`url(#${prefix}-edge)`} strokeWidth="1.8"/>
        <path d="M300 213L357 246L300 279L243 246Z" fill="none" stroke="#d3d8ff" strokeOpacity=".28"/>
        <g fill="none" stroke="#dce2ff" opacity=".18"><path d="M266 233L324 267M278 226L336 260M290 219L348 253M254 240L312 274M267 267L326 233M279 274L338 240M255 260L314 226"/></g>
        <path d="M300 203L375 246L300 290" fill="none" stroke="#f3eaff" strokeOpacity=".6"/>
        <text x="300" y="254" textAnchor="middle" fill="#f7f4ff" fontSize="29" fontWeight="600" letterSpacing="-1" transform="rotate(-1 300 246)">Si</text>
        <path d="M300 343V383M195 284V321L288 375M405 284V321L312 375" fill="none" stroke="#7c8bad" opacity=".35"/>
        <circle cx="300" cy="365" r="2" fill="#a1f1ce"/>
      </g>
    </svg>
    <div className={styles.coreCaption} aria-hidden="true"><span>{selected ? selected.label : "ONE COMMON FOUNDATION"}</span><strong>{selected ? selected.detail : "Extraordinary possibilities."}</strong></div>
    <nav aria-label="Explore application worlds" className={styles.worlds}>
      {worlds.map((world, i) => <Link key={world.id} href={`/applications/?world=${world.id}`} className={styles.world} style={{ "--world-color": world.color, left: `${world.x}%`, top: `${world.y}%` } as CSSProperties} onMouseEnter={()=>setActive(i)} onMouseLeave={()=>setActive(null)} onFocus={()=>setActive(i)} onBlur={()=>setActive(null)} aria-label={`Explore ${world.label}`}>
        <span className={styles.worldIcon}><world.icon size={20} strokeWidth={1.4}/></span><span>{world.label}</span><MoveUpRight size={11} className={styles.worldArrow}/>
      </Link>)}
    </nav>
  </div>;
}

export default function HomepageCover({ snapshot }: { snapshot: Snapshot }) {
  return <section className={`${styles.cover} story-cover`} aria-labelledby="story-title">
    <div className={styles.copy}>
      <div className={styles.eyebrow}><span/>THE SILICON ATLAS <i/> A VISUAL FIELD GUIDE</div>
      <h1 id="story-title">A tiny chip.<br/>An entire<br/><em>economy.</em></h1>
      <p>Inside the technologies changing our world,<br className={styles.desktopBreak}/> there’s a story written in silicon.</p>
      <p className={styles.deck}>Explore the applications. Meet the companies.<br className={styles.desktopBreak}/> Follow the evidence.</p>
      <div className={styles.actions}><a href="#story-worlds" className={styles.primary}>Start the story<span><ArrowDown size={17}/></span></a><Link href="/applications/">Explore all worlds<ArrowUpRight size={15}/></Link></div>
    </div>
    <figure className={styles.figure}><div className={styles.figureLabel}><span>A WORLD BUILT ON SILICON</span><span>INTERACTIVE</span></div><SiliconUniverse/><figcaption><span className={styles.captionDot}/>Choose a world. Discover the silicon inside.<small>Conceptual application map</small></figcaption></figure>
    <div className={styles.foot}><div><span><strong>{snapshot.applications.worlds.length.toString().padStart(2,"0")}</strong>application worlds</span><span><strong>{snapshot.directory.companies.length}</strong>companies to discover</span><span><strong>{snapshot.companies.filter(c=>c.coverage==="financial_pilot").length.toString().padStart(2,"0")}</strong>financial datasets</span></div><a href="#story-worlds">A SMALL COMPONENT. A BIGGER PICTURE.<ArrowDown size={14}/></a></div>
  </section>;
}
