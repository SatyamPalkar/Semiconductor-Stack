"use client";

import { useRef, useState } from "react";
import "./conclusion-map.css";
import { ArrowLeft, ArrowRight, ArrowUpRight, CircleHelp } from "lucide-react";
import Link from "next/link";
import type { Investigation, Metric } from "./research-types";
import { MetricTrace, formatMetric } from "./metric-evidence";

const businesses = [
  { ticker: "NVDA", name: "NVIDIA", role: "DESIGN & PLATFORMS", color: "mint" },
  { ticker: "TSM", name: "TSMC", role: "FOUNDRY & MANUFACTURING", color: "blue" },
];
const chapters = [
  { id: "generated", metric: "operating_cash_flow_margin", title: "Cash generated", label: "Operating cash / revenue", center: "OPERATING CASH", eyebrow: "01 / CASH COMES IN", verb: "generates more", ending: "per revenue unit.", description: "Start before capital investment. Compare operating cash generated per 100 units of each company’s own revenue.", note: "US GAAP and Taiwan IFRS cash-flow classifications have not been harmonized." },
  { id: "investment", metric: "capex_revenue", title: "Capital spending", label: "Disclosed capital spending / revenue", center: "CAPITAL OUTLAYS", eyebrow: "02 / CAPITAL GETS COMMITTED", verb: "discloses more", ending: "capital spending.", description: "Now examine the direct capital-spending burden. The source definitions differ, so this is not a like-for-like asset investment ranking.", note: "NVIDIA includes PPE and intangible purchases; related principal payments are additional. TSMC uses its annual-report capital-expenditure total." },
  { id: "remaining", metric: "free_cash_flow_margin", title: "Cash left", label: "Cash after disclosed capital outlays / revenue", center: "CASH REMAINING", eyebrow: "03 / WHAT REMAINS", verb: "keeps more", ending: "per revenue unit.", description: "The order changes after each company’s disclosed capital outlays. A larger cash residual does not establish a better business or investment.", note: "NVIDIA uses release-defined non-GAAP FCF. TSMC is an analytical residual; other investing and financing flows are excluded. Capital-outlay scopes differ." },
];

function OrbitNode({ business, metric, selected, onSelect, stage }: {
  business: typeof businesses[number]; metric?: Metric; selected: boolean; onSelect: () => void; stage: string;
}) {
  const percentage = metric ? Math.max(0, Math.min(100, Number(metric.value))) : null;
  return <button className={`conclusion-node ${business.color} ${selected ? "selected" : ""} ${metric ? "" : "no-evidence"}`}
    data-company={business.ticker} aria-label={`${business.name} · ${stage} · ${formatMetric(metric)}`}
    aria-pressed={selected} onClick={onSelect}>
    <svg viewBox="0 0 160 160" aria-hidden="true"><circle className="node-track" cx="80" cy="80" r="74"/>{percentage !== null && <circle className="node-arc" cx="80" cy="80" r="74" pathLength="100" strokeDasharray={`${percentage} 100`} transform="rotate(-90 80 80)"/>}</svg>
    <span className="node-company">{business.name}</span><strong>{metric ? formatMetric(metric) : "—"}</strong><span className="node-period">{metric?.fiscal_label || "Unavailable"}</span>
  </button>;
}

export default function ConclusionMap({ periods, nextHref="/briefs/", nextLabel="Continue: Challenge the reading" }: { periods: Investigation["periods"]; nextHref?: string; nextLabel?: string }) {
  const root=useRef<HTMLDivElement>(null);
  const [chapter, setChapter] = useState(0);
  const [selectedCompany, setSelectedCompany] = useState("TSM");
  const current = chapters[chapter];
  const get = (company: string, key = current.metric) => periods.find(p => p.company === company)?.metrics.find(m => m.metric === key);
  const selected = businesses.find(c => c.ticker === selectedCompany)!;
  const selectedMetric = get(selectedCompany);
  const complete = businesses.every(c => get(c.ticker));
  const nvda = get("NVDA"), tsmc = get("TSM");
  const equal = complete && nvda!.value === tsmc!.value;
  const leader = complete ? Number(nvda!.value) > Number(tsmc!.value) ? businesses[0] : businesses[1] : null;
  const profile = periods.find(p => p.company === selectedCompany);
  function advance(next: number) { setChapter(next); root.current?.scrollIntoView({block:"start",behavior:window.matchMedia("(prefers-reduced-motion: reduce)").matches?"instant":"smooth"}); }
  return <div ref={root} className={`conclusion-experience chapter-${current.id}`}>
    <div className="conclusion-chapters" role="group" aria-label="Explore the cash story">
      {chapters.map((item, index) => <button key={item.id} onClick={() => setChapter(index)} aria-label={item.title} aria-pressed={chapter === index}><span aria-hidden="true">0{index + 1}</span>{item.title}{index < 2 && <ArrowRight size={13}/>}</button>)}
    </div>
    <div className="conclusion-story">
      <header className="conclusion-headline" aria-live="polite"><span className="conclusion-eyebrow">{current.eyebrow}</span>
        <h3>{complete ? chapter === 1 ? <>Capital takes<br/><em>different paths.</em></> : equal ? <>The same share.<br/><em>Different businesses.</em></> : <><span className={leader!.color}>{leader!.name}</span> {current.verb}<br/><em>{current.ending}</em></> : <>The evidence<br/><em>stops here.</em></>}</h3>
        <p>{complete ? current.description : "The selected date does not contain both companies’ required evidence. Available figures remain inspectable; no comparative conclusion is drawn."}</p>
      </header>
      <figure className="conclusion-orbit" aria-label={`${current.label} for NVIDIA and TSMC; equal-size company nodes, percentage arcs on a 0–100 scale`}>
        <svg className="orbit-scaffold" viewBox="0 0 760 620" aria-hidden="true">
          <defs><radialGradient id={`orbit-halo-${current.id}`}><stop offset="0" stopColor="#3934b8" stopOpacity=".20"/><stop offset="1" stopColor="#080a12" stopOpacity="0"/></radialGradient></defs>
          <circle cx="380" cy="310" r="300" fill={`url(#orbit-halo-${current.id})`}/>
          {[125, 205, 282].map(r => <circle key={r} cx="380" cy="310" r={r} className="orbit-ring"/>)}
          <path d="M170 190 Q330 180 380 310 Q460 448 590 430" className="orbit-connection"/>
          <path d="M170 190 Q190 460 590 430" className="orbit-connection secondary"/>
          <g className="orbit-stars"><circle cx="380" cy="28" r="4"/><circle cx="98" cy="310" r="3"/><circle cx="662" cy="310" r="3"/><circle cx="380" cy="592" r="4"/><circle cx="508" cy="128" r="3"/><circle cx="252" cy="492" r="3"/></g>
          <text x="380" y="74" textAnchor="middle" className="orbit-category">{current.center}</text>
          <text x="139" y="384" textAnchor="middle" className="orbit-category mint-label">DESIGN</text>
          <text x="611" y="244" textAnchor="middle" className="orbit-category blue-label">FOUNDRY</text>
        </svg>
        <div className="conclusion-center" aria-hidden="true"><span>PER</span><strong>100</strong><span>REVENUE UNITS</span></div>
        {businesses.map(business => <OrbitNode key={business.ticker} business={business} metric={get(business.ticker)} selected={selectedCompany === business.ticker} onSelect={() => setSelectedCompany(business.ticker)} stage={current.title}/>)}
        <figcaption><span><i className="mint-dot"/> NVIDIA</span><span><i className="blue-dot"/> TSMC</span><span>SELECT A NODE TO EXPLORE</span></figcaption>
      </figure>
      <aside className={`conclusion-inspector ${selected.color}`} aria-label="Selected company evidence">
        <div className="inspector-heading"><div><span>{selected.role}</span><h4>{selected.name}</h4></div><ArrowUpRight size={20}/></div>
        <div className="inspector-measure"><strong>{formatMetric(selectedMetric)}</strong><span>{current.label}</span></div>
        <p className="inspector-period">{selectedMetric?.fiscal_label || "Annual observation"} · ended {profile?.period_end}</p>
        {selectedMetric ? <MetricTrace key={`${selectedCompany}-${chapter}-${profile?.period_end}`} metric={selectedMetric}/> : <p className="missing-metric">Unavailable at this research date. Missing evidence is never zero.</p>}
      </aside>
    </div>
    <div className="conclusion-context"><CircleHelp size={16}/><p>{current.note}</p></div>
    <div className="conclusion-story-navigation" aria-label="Cash story navigation"><button disabled={chapter===0} onClick={()=>advance(chapter-1)}><ArrowLeft size={14}/>Previous view</button><span>0{chapter+1} / 03</span>{chapter<2 ? <button onClick={()=>advance(chapter+1)}>Next: {chapters[chapter+1].title}<ArrowRight size={14}/></button> : <Link href={nextHref}>{nextLabel}<ArrowRight size={14}/></Link>}</div>
    <div className="conclusion-map-key"><span>Arcs show percentages on a 0–100 scale. Node size, position and distance are conceptual.</span><Link href="/briefs/">Challenge this reading <ArrowUpRight size={12}/></Link></div>
  </div>;
}
