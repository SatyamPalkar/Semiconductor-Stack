"use client";

import Link from "next/link";
import { useEffect, useRef, useState, type CSSProperties } from "react";
import { ArrowDown, ArrowRight, ArrowUpRight, ChevronLeft, ChevronRight, BookOpen, Layers, Orbit, Waves } from "lucide-react";
import CashInvestigation from "./investigation";
import SiliconScene from "./story-graphics";
import { ApplicationGateway } from "./application-worlds";
import HomepageCover from "./homepage-cover";
import { formatMetric, MetricTrace } from "./metric-evidence";
import type { Metric, Snapshot } from "./research-types";
import "./story.css";

const acts = [
  { id:"story-worlds", label:"Applications", number:"01" },
  { id:"story-system", label:"The system", number:"02" },
  { id:"story-cash", label:"The cash", number:"03" },
  { id:"story-cycle", label:"The changing year", number:"04" },
  { id:"story-next", label:"Your next question", number:"05" },
];
const lenses = [
  { label:"Design", company:"NVIDIA", ticker:"NVDA", color:"#83f4bc", title:"Start with an idea.", body:"What should the chip do? A design business brings research spending, scale and cash generation into focus.", question:"How much of the revenue becomes operating cash?", link:"Explore NVIDIA’s figures" },
  { label:"Fabricate", company:"TSMC", ticker:"TSM", color:"#8aafff", title:"Give the idea a physical form.", body:"A foundry lens puts the factory’s investment burden in view. Follow operating cash, then the disclosed capital outlays.", question:"How much cash remains after capital investment?", link:"Explore TSMC’s figures" },
  { label:"Equip", company:"ASML", ticker:"ASML", color:"#efc16e", title:"Look at the tools behind the factory.", body:"The equipment lens takes the research upstream. Ask what the annual accounts show about cash generation and reinvestment.", question:"What does this equipment business reinvest?", link:"Explore ASML’s figures" },
  { label:"Connect", company:"Amkor", ticker:"AMKR", color:"#b99aff", title:"Bring the pieces together.", body:"Packaging and test add another business model. Its capital footprint and cash definition deserve their own examination.", question:"Are you comparing the same definition of cash?", link:"Explore Amkor’s figures" },
];

function IndustryStory() {
  const [active, setActive] = useState(0);
  const tabs = useRef<(HTMLButtonElement|null)[]>([]);
  const lens = lenses[active];
  function moveTab(index: number) { const next = (index + lenses.length) % lenses.length; setActive(next); tabs.current[next]?.focus(); }
  return <section id="story-system" className="story-act story-system" aria-labelledby="system-heading">
    <div className="story-section-top"><span className="story-overline">02 / MEET THE SYSTEM</span><span>FOUR BUSINESS LENSES</span></div>
    <div className="story-section-heading"><h2 id="system-heading">The same chip.<br/><em>Different bets.</em></h2><p>Before following the money, change your point of view. Each role leads to a different financial question.</p></div>
    <div className="story-lens-tabs" role="tablist" aria-label="Explore the business story">{lenses.map((item,i)=><button ref={el=>{tabs.current[i]=el;}} key={item.ticker} id={`lens-tab-${i}`} role="tab" aria-label={item.label} aria-selected={active===i} tabIndex={active===i?0:-1} aria-controls="business-story-panel" onClick={()=>setActive(i)} onKeyDown={e=>{if(e.key==="ArrowRight"||e.key==="ArrowLeft"){e.preventDefault();moveTab(active+(e.key==="ArrowRight"?1:-1));}if(e.key==="Home"||e.key==="End"){e.preventDefault();moveTab(e.key==="Home"?0:lenses.length-1);}}} style={{"--lens-color":item.color} as CSSProperties}><span>0{i+1}</span><strong>{item.label}</strong><small>{item.company}</small></button>)}</div>
    <div className="story-lens-panel" id="business-story-panel" role="tabpanel" aria-labelledby={`lens-tab-${active}`} style={{"--lens-color":lens.color} as CSSProperties}>
      <figure className="story-lens-figure"><SiliconScene key={active} stage={active}/><figcaption>AI-generated conceptual 3D illustration · business roles, not a verified process or supplier relationship.</figcaption></figure>
      <div className="story-lens-copy" key={lens.ticker}><span className="story-overline">{lens.company} / A RESEARCH LENS</span><h3>{lens.title}</h3><p>{lens.body}</p><div className="story-question"><span>THE QUESTION TO CARRY FORWARD</span><p>{lens.question}</p></div><Link href={`/industry-economics/?company=${lens.ticker}`}>{lens.link}<ArrowUpRight size={16}/></Link></div>
    </div>
    <div className="story-lens-controls"><span>0{active+1} <i>/ 04</i></span><div><button disabled={active===0} onClick={()=>setActive(active-1)} aria-label="Previous business lens"><ChevronLeft size={16}/>Back</button>{active<3 ? <button onClick={()=>setActive(active+1)}>Next: {lenses[active+1].label}<ChevronRight size={16}/></button> : <a href="#story-cash">Now follow the cash<ArrowDown size={16}/></a>}</div></div>
    <div className="story-transition"><span/><p>The business model shapes the question.<br/><strong>The accounts have to answer it.</strong></p><ArrowDown size={20}/></div>
  </section>;
}

function YearStory({ snapshot, asOf }: { snapshot: Snapshot; asOf: string }) {
  const [measure, setMeasure] = useState("gross_margin");
  const observations = snapshot.metrics.filter(m=>m.company==="MU"&&m.metric===measure&&m.inputs.every(i=>i.published_at.slice(0,10)<=asOf)).sort((a,b)=>a.period_end.localeCompare(b.period_end));
  const complete = observations.length===2;
  const signChanged = complete && Number(observations[0].value)<0 && Number(observations[1].value)>0;
  const extent = Math.ceil(Math.max(10,...observations.map(m=>Math.abs(Number(m.value))))/10)*10;
  return <section id="story-cycle" className="story-act story-year" aria-labelledby="year-heading"><div className="story-section-top"><span className="story-overline">04 / CHANGE THE YEAR</span><span>MICRON · TWO ANNUAL OBSERVATIONS</span></div>
    <div className="story-section-heading"><h2 id="year-heading">A snapshot is<br/><em>only one frame.</em></h2><p>Now change the year, not the company. Micron’s selected annual figures show why the reporting period belongs in every conclusion.</p></div>
    <div className="year-story-layout"><div className="year-story-visual"><div className="year-measure-toggle" role="group" aria-label="Memory story measure"><button aria-pressed={measure==="gross_margin"} onClick={()=>setMeasure("gross_margin")}>Gross margin</button><button aria-pressed={measure==="free_cash_flow_margin"} onClick={()=>setMeasure("free_cash_flow_margin")}>Adjusted cash margin</button></div>{complete ? <figure aria-label={`Micron ${measure==="gross_margin"?"gross margin":"adjusted free cash flow margin"}, signed annual observations`}><svg viewBox="0 0 680 310" role="img" aria-label={observations.map(m=>`${m.fiscal_label}: ${formatMetric(m)}`).join("; ")}><line x1="365" y1="45" x2="365" y2="252" stroke="#8b9bb6" strokeWidth="1"/><text x="365" y="28" textAnchor="middle" className="year-chart-axis">0%</text><text x="160" y="279" textAnchor="middle" className="year-chart-axis">−{extent}%</text><text x="570" y="279" textAnchor="middle" className="year-chart-axis">+{extent}%</text>{observations.map((m,i)=>{const value=Number(m.value),width=Math.abs(value)/extent*205,y=76+i*107;return <g key={m.period_end} className={value<0?"year-negative":"year-positive"}><text x="15" y={y+18} className="year-chart-year">{m.fiscal_label}</text><text x="15" y={y+40} className="year-chart-end">{m.period_end}</text><line x1="160" x2="570" y1={y+20} y2={y+20} stroke="#233148"/><rect x={value<0?365-width:365} y={y} width={width} height="40" rx="5" fill={value<0?"#ef8fae":"#83f4bc"}/><text x={value<0?355-width:375+width} y={y+26} textAnchor={value<0?"end":"start"} className="year-chart-value">{formatMetric(m)}</text></g>;})}</svg><div className="year-observation-key">{observations.map(m=><span key={m.period_end}>{m.fiscal_label}<strong className={Number(m.value)<0?"loss":""}>{formatMetric(m)}</strong></span>)}</div><figcaption>{measure==="gross_margin" ? "Gross profit ÷ revenue. Losses keep their sign." : "Micron adjusted free cash flow ÷ revenue. Net capital investment includes its disclosed offsets."}</figcaption></figure> : <div className="year-story-missing" role="status">These Micron observations were not available by the selected research date. The graphic and its interpretation are withheld.</div>}</div>
      <div className="year-story-reading" aria-live="polite"><Waves size={26}/><h3>{signChanged ? "The sign changes.\nThe question gets bigger." : "The story needs\nmore history."}</h3><p>{signChanged ? "The selected measure moves from negative to positive between FY2023 and FY2024. That is a change worth investigating, not enough evidence to declare a durable trend." : "Two selected annual observations cannot establish a full semiconductor cycle. Extend the history before treating a snapshot as a lasting characteristic."}</p><Link href="/industry-economics/?company=MU">Explore both years<ArrowUpRight size={15}/></Link></div></div>
    {complete && <details className="year-story-sources"><summary>Follow these two observations to their source rows</summary><div>{observations.map((m:Metric)=><section key={`${measure}-${m.period_end}`}><h4>{m.fiscal_label} · {formatMetric(m)}</h4><MetricTrace metric={m}/></section>)}</div></details>}
    <div className="story-transition"><span/><p>A different business. A different year.<br/><strong>A better question to ask next.</strong></p><ArrowDown size={20}/></div>
  </section>;
}

export function ChapterOnward({ section }: { section: string }) {
  const next: Record<string,{line:string;label:string;href:string;number:string}> = {
    applications:{line:"You’ve seen the application. Meet the industry behind it.",label:"Explore the company atlas",href:"/value-chain/",number:"02"},
    "value-chain":{line:"You’ve met the players. Now inspect their economics.",label:"Follow the cash",href:"/industry-economics/",number:"02"},
    economics:{line:"Numbers need context. Put the business models beside them.",label:"Compare the companies",href:"/companies/",number:"03"},
    companies:{line:"A result is a beginning. Challenge the explanation.",label:"Read the research note",href:"/briefs/",number:"04"},
    briefs:{line:"Follow the claim back to the original evidence.",label:"Inspect the sources",href:"/sources/#evidence-records",number:"05"},
    sources:{line:"Bring one clear question to the evidence desk.",label:"Ask the evidence",href:"/assistant/",number:"06"},
    assistant:{line:"Return to the story with what you’ve learned.",label:"Back to the beginning",href:"/",number:"01"},
  };
  const item=next[section];
  if(!item)return null;
  return <aside className="chapter-onward" aria-label="Continue the research story"><div className="onward-path" aria-hidden="true"><i/><span/><i/><span/><i/></div><div><span className="story-overline">KEEP THE STORY MOVING / {item.number}</span><p>{item.line}</p></div><Link href={item.href}>{item.label}<ArrowRight size={20}/></Link></aside>;
}

export default function StoryOverview({ snapshot, asOf }: { snapshot: Snapshot; asOf: string; onSource: () => void }) {
  const root=useRef<HTMLDivElement>(null);
  const [active,setActive]=useState(acts[0].id);
  useEffect(()=>{
    const masthead=document.querySelector('.atlas-masthead');
    const resize=new ResizeObserver(()=>{if(masthead&&root.current)root.current.style.setProperty('--story-header-height',`${masthead.getBoundingClientRect().height}px`);});
    if(masthead)resize.observe(masthead);
    const observer=new IntersectionObserver(entries=>{for(const entry of entries)if(entry.isIntersecting)setActive(entry.target.id);},{rootMargin:'-25% 0px -55% 0px',threshold:0});
    for(const act of acts){const element=document.getElementById(act.id);if(element)observer.observe(element);}
    return()=>{resize.disconnect();observer.disconnect();};
  },[]);
  useEffect(()=>{
    const rail=root.current?.querySelector<HTMLElement>(".story-chapter-rail");
    const link=rail?.querySelector<HTMLElement>('[aria-current="location"]');
    if(rail&&link)rail.scrollTo({left:Math.max(0,link.offsetLeft-(rail.clientWidth-link.clientWidth)/2),behavior:window.matchMedia("(prefers-reduced-motion: reduce)").matches?"instant":"smooth"});
  },[active]);
  return <div ref={root} className="guided-story visual-investigation-home">
    <HomepageCover snapshot={snapshot}/>
    <nav className="story-chapter-rail" aria-label="Story chapters">{acts.map(act=><a key={act.id} href={`#${act.id}`} aria-current={active===act.id?'location':undefined}><span>{act.number}</span>{act.label}<i/></a>)}</nav>
    <div className="story-reading-width"><ApplicationGateway catalog={snapshot.applications}/><IndustryStory/>
      <section className="story-act story-cash" id="story-cash" aria-label="Cash story chapter"><div className="story-section-top"><span className="story-overline">03 / FOLLOW WHAT REMAINS</span><span>FROM THE BUSINESS MODEL TO THE ACCOUNTS</span></div><p className="story-cash-intro">Revenue starts the story.<br/><em>Cash changes the ending.</em></p><CashInvestigation data={snapshot.investigation} asOf={asOf} compact hero nextHref="#story-cycle" nextLabel="Next: Change the year"/></section>
      <YearStory snapshot={snapshot} asOf={asOf}/>
      <section id="story-next" className="story-act story-next" aria-labelledby="next-heading"><span className="story-overline">05 / MAKE IT YOUR INVESTIGATION</span><h2 id="next-heading">Every conclusion<br/>opens <em>another question.</em></h2><div className="story-next-paths">{[{icon:Orbit,title:"Who else is in the picture?",text:`Explore ${snapshot.directory.companies.length} companies and businesses across the industry.`,href:"/value-chain/",label:"Map the industry"},{icon:Layers,title:"How do other businesses compare?",text:"Inspect six financial datasets, with their own currencies and cash definitions.",href:"/companies/",label:"Explore the economics"},{icon:BookOpen,title:"What could change the explanation?",text:"Read the counterevidence, alternative explanations and questions still open.",href:"/briefs/",label:"Challenge the story"},{icon:ArrowUpRight,title:"Where does the evidence lead?",text:`Find ${snapshot.directory.resources.length} research resources or inspect the stored financial sources.`,href:"/sources/",label:"Follow the sources"}].map(path=><Link href={path.href} key={path.href}><path.icon size={25}/><div><h3>{path.title}</h3><p>{path.text}</p><span>{path.label}</span></div><ArrowUpRight size={23}/></Link>)}</div></section>
    </div>
  </div>;
}
