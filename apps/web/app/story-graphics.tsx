"use client";

import { useId } from "react";

/** Illustrative geometry only: no process dimensions or supplier relationships. */
export default function SiliconScene({ stage = 0, cover = false }: { stage?: number; cover?: boolean }) {
  const id = useId().replaceAll(":", "");
  const color = ["#83f4bc", "#8aafff", "#efc16e", "#b99aff"][stage];
  return <svg className={`silicon-scene scene-${stage} ${cover ? "scene-cover" : ""}`} viewBox="0 0 700 470" role="img" aria-label={cover ? "Illustrated chip layers surrounded by design, fabrication, equipment and packaging roles" : ["Illustrated circuit design and chip architecture", "Illustrated wafer with an array of chip dies", "Illustrated light beam over a semiconductor wafer", "Illustrated stack of connected chip layers"][stage]}>
    <defs>
      <radialGradient id={`${id}-halo`}><stop stopColor={color} stopOpacity=".18"/><stop offset="1" stopColor={color} stopOpacity="0"/></radialGradient>
      <linearGradient id={`${id}-surface`} x1="0" y1="0" x2="1" y2="1"><stop stopColor={color} stopOpacity=".3"/><stop offset="1" stopColor="#0c1122"/></linearGradient>
      <pattern id={`${id}-wafer`} width="33" height="33" patternUnits="userSpaceOnUse"><rect x="3" y="3" width="26" height="26" rx="3" fill={color} fillOpacity=".13" stroke={color} strokeOpacity=".4" strokeWidth=".7"/></pattern>
      <clipPath id={`${id}-circle`}><ellipse cx="350" cy="269" rx="204" ry="111"/></clipPath>
      <linearGradient id={`${id}-beam`} x1="0" y1="0" x2="0" y2="1"><stop stopColor={color} stopOpacity=".05"/><stop offset="1" stopColor={color} stopOpacity=".55"/></linearGradient>
    </defs>
    <ellipse cx="350" cy="254" rx="340" ry="215" fill={`url(#${id}-halo)`}/>
    <g fill="none" stroke="#435474" strokeWidth=".8" strokeDasharray="2 8" opacity=".55"><ellipse cx="350" cy="288" rx="300" ry="148"/><ellipse cx="350" cy="288" rx="264" ry="130"/><path d="M40 288H660M350 100V454"/></g>
    {(cover || stage === 0 || stage === 3) ? <g className="silicon-stack">
      <g transform="translate(350 294) matrix(1 .48 -1 .48 0 0)">
        <rect x="-160" y="-160" width="320" height="320" rx="20" fill="#0d1721" stroke="#304657"/>
        {Array.from({length:7},(_,i) => <g key={i} fill="none" stroke={color} strokeWidth="1" opacity=".35"><path d={`M${-120+i*39} -152v37l${i%2?15:-15} 15v55M${-120+i*39} 152v-37l${i%2?15:-15} -15v-55`}/><path d={`M-152 ${-120+i*39}h37l15 ${i%2?15:-15}h55M152 ${-120+i*39}h-37l-15 ${i%2?15:-15}h-55`}/></g>)}
        {Array.from({length:8},(_,i) => <g key={i} fill={color} opacity=".55"><circle cx={-136+i*39} cy="-143" r="3"/><circle cx={-136+i*39} cy="143" r="3"/></g>)}
      </g>
      {[0,1,2].map((layer) => <g key={layer} transform={`translate(350 ${274-layer*29}) matrix(1 .48 -1 .48 0 0)`}><rect x={-91-layer*5} y={-91-layer*5} width={182+layer*10} height={182+layer*10} rx="8" fill="#10182b" stroke={color} strokeOpacity={.3+layer*.2} strokeWidth="1.3"/>{stage===3 && Array.from({length:5},(_,i) => <path key={i} d={`M${-75+i*37} -92v184`} stroke={color} strokeOpacity=".15"/>)}</g>)}
      <g transform="translate(350 183) matrix(1 .48 -1 .48 0 0)"><rect x="-83" y="-83" width="166" height="166" rx="9" fill={`url(#${id}-surface)`} stroke={color} strokeWidth="1.6"/>{Array.from({length:4},(_,x)=>Array.from({length:4},(_,y)=><rect key={`${x}-${y}`} x={-65+x*34} y={-65+y*34} width="28" height="28" rx="3" fill={color} fillOpacity={(x+y)%3===0?.23:.07} stroke={color} strokeOpacity=".2"/>))}</g>
      <g fill="none" stroke={color} strokeWidth="1.4" strokeDasharray="5 9" className="scene-signals" opacity=".7"><path d="M64 294L181 237L241 267"/><path d="M459 267L521 237L637 294"/></g>
      <text x="350" y="189" textAnchor="middle" fill="#edf5ff" fontSize="26" letterSpacing="3">Si</text>
    </g> : <g className="silicon-wafer">
      <ellipse cx="350" cy="281" rx="204" ry="111" fill="#101d35" stroke="#344f7e"/>
      <ellipse cx="350" cy="269" rx="204" ry="111" fill="#0b1425" stroke={color} strokeOpacity=".8"/>
      <g clipPath={`url(#${id}-circle)`}><rect x="130" y="140" width="440" height="250" fill={`url(#${id}-wafer)`}/><path d="M146 261H554" stroke={color} strokeOpacity=".5" className="wafer-scan"/></g>
      {stage===2 && <g><path d="M300 73L320 266H380L400 73Z" fill={`url(#${id}-beam)`}/><ellipse cx="350" cy="74" rx="50" ry="18" fill="#121c2b" stroke={color}/><ellipse cx="350" cy="266" rx="30" ry="12" fill={color} fillOpacity=".45"/><path d="M290 42h120v30M315 42V20h70v22" fill="none" stroke={color} strokeOpacity=".5"/></g>}
      {stage===1 && <g fill="none" stroke={color}><rect x="284" y="215" width="64" height="64" rx="5" strokeWidth="2"/><path d="M284 207v-15h64v15M273 215h-14v64h14" strokeOpacity=".6"/></g>}
    </g>}
    {cover ? <g className="scene-labels" fill="#9fb0c9" fontSize="11" letterSpacing="2"><text x="103" y="116">DESIGN</text><text x="475" y="116">FABRICATE</text><text x="96" y="405">EQUIP</text><text x="477" y="405">CONNECT</text><g fill={color}><circle cx="85" cy="112" r="3"/><circle cx="459" cy="112" r="3"/><circle cx="78" cy="401" r="3"/><circle cx="460" cy="401" r="3"/></g></g> : <g fill="#8fa3c4" fontSize="10" letterSpacing="2"><text x="350" y="436" textAnchor="middle">{["IDEAS → ARCHITECTURE", "CAPITAL → PHYSICAL CAPABILITY", "TOOLS → MANUFACTURING CAPABILITY", "COMPONENTS → CONNECTED SYSTEM"][stage]}</text></g>}
  </svg>;
}
