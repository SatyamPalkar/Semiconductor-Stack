"use client";
import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { ArrowUpRight, Check, CircleDot, Cpu, Database, ExternalLink, FileText, FlaskConical, Menu, RefreshCw, Search, ShieldCheck, X } from "lucide-react";
import FinancialChart from "./chart";
import { CashLens, FinancialCoverage } from "./financial-lens";

import type { Metric, Source, Snapshot, Answer } from "./research-types";
import StoryOverview, { ChapterOnward } from "./story";
import IndustryAtlas, { ResourceLibrary } from "./industry-atlas";
import ApplicationExplorer from "./application-worlds";
import CashInvestigation, { ResearchBrief } from "./investigation";
import { MetricTrace, formatMetric, metricLabel } from "./metric-evidence";

const navigation = [
  { key: "overview", href: "/", label: "Overview" },
  { key: "applications", href: "/applications/", label: "Applications" },
  { key: "value-chain", href: "/value-chain/", label: "Industry atlas" },
  { key: "economics", href: "/industry-economics/", label: "Cash economics" },
  { key: "companies", href: "/companies/", label: "Company comparison" },
  { key: "assistant", href: "/assistant/", label: "Research assistant" },
  { key: "briefs", href: "/briefs/", label: "Research briefs" },
  { key: "sources", href: "/sources/", label: "Sources & resources" },
];
const headings: Record<string, [string, string]> = {
  applications: ["Where the world meets silicon.", "Explore the tasks, chip functions and company capabilities behind AI, mobility, infrastructure and more."],
  "value-chain": ["Explore the semiconductor universe.", "Companies, business models and official research starting points across the industry."],
  economics: ["Inspect each business over time.", "Two annual observations in the company’s own currency. No invented interim history."],
  companies: ["Different businesses. Different cash economics.", "Explore six historical financial datasets, then examine the focused NVIDIA and TSMC comparison."],
  assistant: ["Put the evidence to work.", "Use the research desk to trace a figure, inspect its source and identify what remains unknown."],
  briefs: ["What the cash comparison can tell us.", "A bounded conclusion, the evidence against a simple explanation and what would change it."],
  sources: ["The semiconductor research library.", "Explore official resources or inspect the financial evidence already stored in this project."],
};

function apiOrigin() {
  const configured = process.env.NEXT_PUBLIC_API_BASE;
  const origin = configured || (["localhost", "127.0.0.1"].includes(window.location.hostname) ? "http://127.0.0.1:8100" : "");
  if (!origin) return "";
  try { const url = new URL(origin); return ((url.protocol === "https:" || (url.protocol === "http:" && ["127.0.0.1", "localhost"].includes(url.hostname))) && !url.username && !url.password && !url.search && !url.hash && url.pathname === "/") ? url.origin : ""; } catch { return ""; }
}
function pretty(value: string) { return value.replaceAll("_", " "); }

export default function Platform({ section }: { section: string }) {
  const [snapshot, setSnapshot] = useState<Snapshot | null>(null);
  const [error, setError] = useState("");
  const [asOf, setAsOf] = useState("2025-03-13");
  const [deskCompany, setDeskCompany] = useState("NVDA");
  const [chartCompany, setChartCompany] = useState("NVDA");
  const financialCompanies = snapshot?.companies.filter(c => c.coverage === "financial_pilot") || [];
  const deskName = financialCompanies.find(c => c.ticker === deskCompany)?.name || deskCompany;
  const deskYear = snapshot?.metrics.filter(m => m.company === deskCompany && m.metric === "revenue").at(-1)?.fiscal_label || "FY2025";
  const chartName = financialCompanies.find(c => c.ticker === chartCompany)?.name || chartCompany;
  const chartCurrency = snapshot?.metrics.find(m => m.company === chartCompany)?.currency || "USD";
  const exampleQuestions = [`What was ${deskName} gross margin in ${deskYear}?`, `What was ${deskName} free cash flow in ${deskYear}?`, `What was ${deskName} revenue growth in ${deskYear}?`];
  const [api, setApi] = useState<"checking" | "offline" | "extractive" | "live">("checking");
  const [sourceOpen, setSourceOpen] = useState(false);
  const [mobileNav, setMobileNav] = useState(false);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState<Answer | null>(null);
  const [questionError, setQuestionError] = useState("");
  const [busy, setBusy] = useState(false);
  const [sourceSearch, setSourceSearch] = useState("");
  const [sourceView, setSourceView] = useState("resources");
  const [liveMode, setLiveMode] = useState(false);
  const [recorded, setRecorded] = useState(false);
  const [runTests, setRunTests] = useState(false);
  useEffect(() => { try { const saved = window.sessionStorage.getItem("semiscope-research-asof"); if (saved && /^\d{4}-\d{2}-\d{2}$/.test(saved)) setAsOf(saved); } catch {} if (window.location.hash === "#evidence-records") setSourceView("evidence"); fetch("/research-snapshot.json").then(r => { if (!r.ok) throw Error(); return r.json(); }).then(setSnapshot).catch(() => setError("The research snapshot could not be loaded. Run the database export command and rebuild the site.")); }, []);
  async function checkAPI() {
    setApi("checking"); const origin = apiOrigin(); if (!origin) { setApi("offline"); return; }
    try { const r = await fetch(`${origin}/api/health`, { signal: AbortSignal.timeout(3000) }); if (!r.ok) throw Error(); const data = await r.json(); setApi(data.live_ai_available ? "live" : "extractive"); } catch { setApi("offline"); }
  }
  useEffect(() => { void checkAPI(); const requested = new URLSearchParams(window.location.search).get("company"); if (requested && ["NVDA", "TSM", "ASML", "MU", "TXN", "AMKR"].includes(requested)) setChartCompany(requested); }, []);
  const eligibleSources = snapshot?.sources.filter(s => s.published_at.slice(0, 10) <= asOf) || [];
  const values = snapshot?.metrics.filter(m => m.inputs.every(i => i.published_at.slice(0, 10) <= asOf)) || [];
  const metric = (name: string, year = deskYear, company = deskCompany) => values.find(m => m.company === company && m.metric === name && m.fiscal_label === year);
  const revenueChart = useMemo(() => values.filter(m => m.company === chartCompany && m.metric === "revenue").map(m => ({ year: m.fiscal_label, value: Number(m.value) * m.unit_scale / 1e9 })), [snapshot, asOf, chartCompany]);
  const marginChart = useMemo(() => values.filter(m => m.company === chartCompany && m.metric === "gross_margin").map(m => ({ year: m.fiscal_label, value: Number(m.value) })), [snapshot, asOf, chartCompany]);

  const heading = headings[section];
  async function ask(q: string, example = false) {
    setQuestion(q); setQuestionError(""); setAnswer(null); setRecorded(false);
    if (api === "offline") {
      if (!example) { setQuestionError("The API is offline. Free-form retrieval needs the backend. You can still inspect a recorded calculation below."); return; }
      const key = q.includes("gross margin") ? "gross_margin" : q.includes("free cash flow") ? "free_cash_flow" : "revenue_growth";
      const m = metric(key); if (!m) { setQuestionError("This calculation was not available as of the selected date."); return; }
      setRecorded(true); setAnswer({ mode: "recorded_calculation", abstained: false, as_of: asOf, model_calls: 0, citation_support: "Previously computed from PostgreSQL facts; no live retrieval or LLM generation.", evidence: m.inputs.map((i, index) => ({ citation_id: index + 1, source_id: i.source_id, title: i.source_title, text: `${metricLabel(i.metric)}: ${i.value} ${i.currency} at original scale ${i.unit_scale}`, locator: i.locator, url: i.url, published_at: i.published_at })), paragraphs: [{ text: `${deskName} ${m.fiscal_label} ${m.label || pretty(m.metric)} was ${m.value} ${m.unit} (annual period ended ${m.period_end}). ${m.definition}`, citations: m.inputs.map((_, i) => i + 1), classification: m.classification }] }); return;
    }
    setBusy(true);
    try { const response = await fetch(`${apiOrigin()}/api/questions`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ question: q, filters: { company: deskCompany, as_of: asOf }, mode: liveMode ? "live" : "extractive" }), signal: AbortSignal.timeout(35000) }); const data = await response.json(); if (!response.ok) throw new Error(typeof data.detail === "string" ? data.detail : "The question could not be processed."); setAnswer(data); }
    catch (err) { setQuestionError(err instanceof Error ? err.message : "The API did not respond. No fallback answer was generated."); }
    finally { setBusy(false); }
  }
  return <div className={`platform atlas ${section === "overview" ? "atlas-home" : "atlas-detail"}`}>
    <header className="atlas-masthead">
      <div className="atlas-masthead-inner">
        <Link href="/" className="atlas-wordmark" aria-label="Semiscope research home">semi<span>scope</span><i aria-hidden="true"/></Link>
        <div className="atlas-edition"><span>INDEPENDENT RESEARCH</span><strong>THE SILICON ATLAS</strong></div>
        <div className="atlas-header-actions"><label className="asof">FINANCIAL AS OF <input aria-label="Research as-of date" type="date" value={asOf} disabled={busy} onChange={e => { setAsOf(e.target.value); try { window.sessionStorage.setItem("semiscope-research-asof", e.target.value); } catch {} setAnswer(null); }}/></label><button className="atlas-menu-button" onClick={() => setMobileNav(!mobileNav)} aria-label="Toggle navigation" aria-expanded={mobileNav}>{mobileNav ? <X size={20}/> : <Menu size={20}/>}</button></div>
      </div>
      <nav className={`atlas-navigation ${mobileNav ? "is-open" : ""}`} aria-label="Main navigation">{navigation.map((n, i) => <Link aria-label={n.label} aria-current={n.key === section ? "page" : undefined} href={n.href} key={n.key} onClick={() => setMobileNav(false)}><span>{String(i+1).padStart(2,"0")}</span>{n.label}<ArrowUpRight size={12}/></Link>)}</nav>
    </header>
    <main>
      <div className="content">
        {section !== "overview" && <section className="atlas-page-title"><div className="atlas-kicker"><span>{String(navigation.findIndex(n => n.key === section)+1).padStart(2,"0")} / THE RESEARCH ATLAS</span><span>{["applications", "value-chain", "sources"].includes(section) ? "GLOBAL DISCOVERY / LOCAL EVIDENCE" : "HISTORICAL FINANCIAL INVESTIGATION"}</span></div><h1>{heading[0]}</h1><p>{heading[1]}</p></section>}
        {error && <div className="notice error" role="alert">{error}</div>}{!snapshot && !error && <div className="loading" role="status">Loading the research snapshot…</div>}
        {snapshot && <>
        {!["overview", "value-chain", "applications"].includes(section) && (section !== "sources" || sourceView === "evidence") && <div className="snapshot-note"><div><CircleDot size={13}/><span><strong>Historical source snapshot</strong> · Native currencies and units · Company-specific annual calendars</span></div><button onClick={() => setSourceOpen(true)}>Provenance <ArrowUpRight size={12}/></button></div>}
        {!eligibleSources.length && !["value-chain", "applications"].includes(section) && (section !== "sources" || sourceView === "evidence") && <div className="notice" role="status">No financial source was available by this selected date. Metrics are withheld rather than filled with future publications.</div>}
        {section === "overview" && <StoryOverview snapshot={snapshot} asOf={asOf} onSource={() => setSourceOpen(true)} />}
        {section === "applications" && <ApplicationExplorer catalog={snapshot.applications} directory={snapshot.directory}/>}
        {section === "value-chain" && <IndustryAtlas directory={snapshot.directory}/> }
        {section === "economics" && <><div className="table-toolbar"><label>Company <select aria-label="Financial chart company" value={chartCompany} onChange={e => setChartCompany(e.target.value)}>{financialCompanies.map(c => <option value={c.ticker} key={c.ticker}>{c.name}</option>)}</select></label><span>Two annual observations · not a full-cycle study</span></div><CashLens values={values} company={chartCompany}/><div className="two-columns"><div className="panel"><span className="eyebrow">REVENUE</span><h3>{chartName} annual revenue<span className="chart-unit">{chartCurrency} billion</span></h3><FinancialChart data={revenueChart} label={`Annual ${chartName} revenue by fiscal year in ${chartCurrency} billions`} currency={chartCurrency}/><SourceLine onOpen={() => setSourceOpen(true)}/></div><div className="panel"><span className="eyebrow">PROFITABILITY</span><h3>Gross margin<span className="chart-unit">Percent of revenue</span></h3><FinancialChart data={marginChart} label={`${chartName} gross margin by fiscal year`} percent/><SourceLine onOpen={() => setSourceOpen(true)}/></div></div><details className="evidence-drawer"><summary>Inspect all annual metrics and source calculations</summary><MetricTable values={values.filter(m => m.company === chartCompany)} company={chartName}/></details><div className="notice">Revenue growth is calculated in each company’s reporting currency. The two annual observations do not explain a complete semiconductor cycle, and supply-chain revenues must not be added into a market-size estimate.</div></>}
        {section === "companies" && <><FinancialCoverage companies={financialCompanies} values={values}/><CashInvestigation data={snapshot.investigation} asOf={asOf}/><div className="directory-cross-link"><span><strong>{snapshot.directory.companies.length} companies & businesses in the atlas</strong>Directory listings are separate from verified financial coverage.</span><Link href="/value-chain/">Explore the industry <ArrowUpRight size={15}/></Link></div></>}
        {section === "assistant" && <><div className="assistant-layout"><section className="panel chat-panel"><div className="panel-heading"><div><span className="eyebrow">YOUR EVIDENCE DESK</span><h3>Ask the research assistant</h3></div><span className="subtle-badge"><span className="tiny-dot"/>{api === "checking" ? "Connecting" : api === "offline" ? "Snapshot mode" : "API connected"}</span></div><p className="muted">Trace a supported annual figure for any of the six loaded companies. This bounded evidence desk does not generate the investigation or answer general industry questions. Calculations use PostgreSQL facts; extractive answers make no hosted model calls.</p><label className="desk-company">Company <select aria-label="Evidence desk company" disabled={busy} value={deskCompany} onChange={e => { setDeskCompany(e.target.value); setAnswer(null); setQuestion(""); setQuestionError(""); }}>{financialCompanies.map(c => <option value={c.ticker} key={c.ticker}>{c.name}</option>)}</select></label><p className="small-note">For a two-company argument, <Link className="text-link" href="/companies/">read the qualified comparison</Link>. TSMC cash after capital outlays is an analytical residual, with a different scope from NVIDIA release-defined FCF.</p><form onSubmit={e => { e.preventDefault(); void ask(question); }}><label className="sr-only" htmlFor="research-question">Research question</label><textarea id="research-question" value={question} onChange={e => setQuestion(e.target.value)} placeholder={`What was ${deskName} free cash flow in ${deskYear}?`} maxLength={1200} required/><div className="composer-actions"><span><Database size={13}/> {deskCompany} · {asOf}</span><button className="button primary" disabled={busy || !question.trim()}>{busy ? "Tracing the evidence…" : "Ask question"}<ArrowUpRight size={16}/></button></div></form><div className="example-list"><span>{api === "offline" ? "INSPECT A RECORDED CALCULATION" : "TRY A QUESTION"}</span>{exampleQuestions.map(q => <button key={q} disabled={busy} onClick={() => void ask(q, true)}>{q}<ArrowUpRight size={13}/></button>)}</div>{api === "live" && <label className="live-toggle"><input type="checkbox" checked={liveMode} onChange={e => setLiveMode(e.target.checked)}/> Enable hosted model for non-calculation answers. Evidence and question will be sent to Groq.</label>}{questionError && <div role="alert" className="notice error">{questionError}</div>}{answer && <article className="answer-panel" aria-live="polite"><div className="answer-label"><span><ShieldCheck size={15}/>{recorded ? "Recorded calculation · no live AI" : pretty(answer.mode)}</span><small>{answer.model_calls} model calls</small></div>{answer.abstained ? <><h3>There is not enough evidence for that answer.</h3><p>{answer.limitation}</p></> : answer.paragraphs.map((p, i) => <div key={i}><span className="classification">{pretty(p.classification)}</span><p>{p.text} {p.citations.map(c => <a href={`#evidence-${c}`} key={c} className="citation">[{c}]</a>)}</p></div>)}{answer.evidence.map(e => <details key={e.citation_id} id={`evidence-${e.citation_id}`} className="evidence"><summary>Source {e.citation_id} · {e.title}</summary><p>{e.text}</p><small>{e.locator}</small><a href={e.url} target="_blank" rel="noreferrer">Original source <ExternalLink size={12}/></a></details>)}<p className="small-note">{answer.citation_support}{answer.latency_ms !== undefined ? ` · ${answer.latency_ms.toFixed(0)} ms` : ""}</p></article>}</section><aside className="assistant-guide"><div className="panel"><span className="eyebrow">CLEAR BOUNDARIES</span><h3>Evidence before eloquence.</h3>{["Source IDs resolve to stored evidence.", "Financial arithmetic runs in Python.", "Publication dates bound the as-of view.", "Missing evidence stays missing."].map(t => <p key={t}><Check size={14}/>{t}</p>)}</div><div className="panel"><span className="eyebrow">CONNECTION</span><h3>{api === "offline" ? "Backend offline" : api === "live" ? "Hosted model configured" : "Credential-free extractive mode"}</h3><p className="muted">{api === "offline" ? "The static research and recorded calculations remain usable. Start the local API for new questions." : "Financial tools and local embeddings work without an API key. Live model generation is opt-in."}</p><button className="text-link" onClick={checkAPI}><RefreshCw size={13}/> Check connection</button></div></aside></div></>}
        {section === "briefs" && <ResearchBrief data={snapshot.investigation} asOf={asOf}/>}
        {section === "sources" && <div className="source-view-tabs" role="group" aria-label="Source library view"><button aria-pressed={sourceView === "resources"} onClick={() => setSourceView("resources")}>Research resources ({snapshot.directory.resources.length})</button><button aria-pressed={sourceView === "evidence"} onClick={() => setSourceView("evidence")}>Ingested evidence ({eligibleSources.length})</button></div>}
        {section === "sources" && sourceView === "resources" && <ResourceLibrary directory={snapshot.directory}/>}
        {section === "sources" && sourceView === "evidence" && <><div className="table-toolbar"><div><Database size={16}/> Source library <span>{eligibleSources.length} available as of {asOf}</span></div><label className="search-field"><Search size={14}/><input aria-label="Search sources" value={sourceSearch} onChange={e => setSourceSearch(e.target.value)} placeholder="Find a source…"/></label></div>{eligibleSources.filter(s => `${s.title} ${s.publisher}`.toLowerCase().includes(sourceSearch.toLowerCase())).map(s => <SourceCard key={s.id} source={s}/>)}{!eligibleSources.filter(s => `${s.title} ${s.publisher}`.toLowerCase().includes(sourceSearch.toLowerCase())).length && <div className="notice">No source matches this search and as-of date.</div>}<div className="two-columns methodology"><div className="panel"><span className="eyebrow">FINANCIAL DEFINITIONS</span><h3>Know the denominator.</h3><label className="desk-company">Definitions for <select aria-label="Definition company" value={chartCompany} onChange={e => setChartCompany(e.target.value)}>{financialCompanies.map(c => <option value={c.ticker} key={c.ticker}>{c.name}</option>)}</select></label>{snapshot.metrics.filter(m => m.company === chartCompany).filter((m, index, all) => all.findIndex(other => other.metric === m.metric) === index).map(m => <details key={m.metric}><summary>{metricLabel(m.metric)}</summary><p>{m.definition}</p></details>)}</div><div className="panel"><span className="eyebrow">EVALUATION</span><h3>What has actually been checked?</h3><p>{snapshot.evaluation.executed ? `${snapshot.evaluation.passed} of ${snapshot.evaluation.total} executed milestone-1 development checks passed. This dataset covers the original NVIDIA pilot; it does not score the TSMC investigation.` : "No evaluation results are available yet."}</p><p className="muted">Model evaluation and human citation-support review are pending. Automated checks cover numerical accuracy, source resolution, publication-date filtering and appropriate abstention; they do not establish investment merit.</p><button className="text-link" onClick={() => setRunTests(!runTests)}><FlaskConical size={14}/>{runTests ? "Hide" : "Show"} evaluation scope</button>{runTests && <div className="notice">{snapshot.evaluation.kind || "Run the local evaluation command to generate a result artifact."}<br/>Human-reviewed: {snapshot.evaluation.human_reviewed ? "yes" : "pending"}. Agent comparison: not implemented.</div>}<h4>Known limitations</h4><ul className="limitations">{snapshot.limitations.map(l => <li key={l}>{l}</li>)}</ul></div></div></>}
        <ChapterOnward section={section}/><p className="small-note snapshot-freshness">{section === "applications" ? `Application guide curated ${snapshot.applications.reviewed_on} · Financial evidence cutoff` : "Historical evidence cutoff"}: {snapshot.research_as_of} · Snapshot generated {snapshot.generated_at.slice(0, 10)}. The selected date filters financial figures; application guides are separately dated. No newer financial disclosures are fetched. Independent human review pending.</p><footer className="page-footer"><span><Cpu size={13}/> SEMICONDUCTOR RESEARCH PLATFORM</span><p>A question. An investigation. A source.</p><span>THE SILICON ATLAS / No. 001</span></footer>
        </>}
      </div>
    </main>
    {sourceOpen && <div className="modal-backdrop" onClick={() => setSourceOpen(false)}><section className="source-modal" role="dialog" aria-modal="true" aria-label="Source provenance" onClick={e => e.stopPropagation()}><div className="panel-heading"><div><span className="eyebrow">FOLLOW THE EVIDENCE</span><h2>Source provenance</h2></div><button className="icon-button" onClick={() => setSourceOpen(false)} aria-label="Close source details"><X size={20}/></button></div>{eligibleSources.map(s => <SourceCard key={s.id} source={s}/>)}{!eligibleSources.length && <p>No sources are available as of this date.</p>}<p className="small-note">Static values were exported from PostgreSQL. The online API queries the database; the browser does not become the financial system of record.</p></section></div>}
  </div>;
}

function SourceLine({ onOpen }: { onOpen: () => void }) { return <div className="chart-source"><span>Company-specific accounting basis · annual periods</span><button onClick={onOpen}>Financial sources <ExternalLink size={11}/></button></div>; }
function MetricTable({ values, company }: { values: Metric[]; company: string }) { const years = [...new Set(values.filter(m => m.metric === "revenue").map(m => m.fiscal_label))]; const keys = ["revenue", "revenue_growth", "gross_margin", "operating_margin", "operating_cash_flow", "operating_cash_flow_margin", "capex_revenue", "rd_revenue", "free_cash_flow", "free_cash_flow_margin"]; return <div className="panel table-panel"><div className="panel-heading"><div><span className="eyebrow">{company} · {values[0]?.accounting_basis || "No eligible evidence"}</span><h3>Reported facts. Reproducible calculations.</h3></div></div><table><thead><tr><th>Metric</th>{years.map(year => <th key={year}>{year}</th>)}</tr></thead><tbody>{keys.map(key => <tr key={key}><th scope="row">{metricLabel(key)}</th>{years.map(year => { const m = values.find(v => v.metric === key && v.fiscal_label === year); return <td key={year}><strong>{formatMetric(m)}</strong><MetricTrace metric={m}/></td>; })}</tr>)}</tbody></table><p className="small-note table-note">Unavailable means missing evidence, never zero. Cash-flow and capital-spending scope is company-specific; inspect each definition before comparing.</p></div>; }
function SourceCard({ source }: { source: Source }) { return <article className="panel source-card"><div className="source-icon"><FileText size={23}/></div><div><span className="eyebrow">PRIMARY SOURCE · {source.company}</span><h3>{source.title}</h3><p>{source.publisher} · {source.company === "TSM" && source.title.includes("annual report") ? "report printed" : "published"} {source.publication_date || source.published_at.slice(0, 10)} · captured {source.retrieved_at.slice(0, 10)}</p><div className="source-tags"><span>{source.accounting_basis}</span><span>{pretty(source.capture_kind)}</span></div><details><summary>Checksum & record details</summary><code>{source.checksum}</code><small>{source.id}</small><p>Date-only source dates use the end of the publisher’s day as an availability cutoff. TSMC annual reports use their printed date; independent historical availability is unverified. These later captures are not certified historical archives.</p></details><a className="text-link" href={source.url} target="_blank" rel="noreferrer">Open original source <ExternalLink size={13}/></a></div></article>; }
