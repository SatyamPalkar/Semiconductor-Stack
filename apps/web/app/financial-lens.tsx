"use client";
import Link from "next/link";
import { useState } from "react";
import type { Company, Metric } from "./research-types";
import { formatMetric, MetricTrace } from "./metric-evidence";
import "./financial-lens.css";

export function FinancialCoverage({ companies, values }: { companies: Company[]; values: Metric[] }) {
  return <section className="financial-coverage-grid" aria-label="Financial dataset coverage"><div className="financial-lens-heading"><span className="directory-eyebrow">SIX COMPANY DATASETS</span><h2>Choose a business. Follow its cash.</h2><p>Historical annual observations in native currencies. Each dataset has its own capital-spending definition.</p></div><div className="financial-company-grid">{companies.map(company => { const revenue = values.filter(m => m.company === company.ticker && m.metric === "revenue").at(-1); return <Link key={company.ticker} href={`/industry-economics/?company=${company.ticker}`}><span>{company.layer}</span><h3>{company.name}</h3><strong>{formatMetric(revenue)}</strong><small>{revenue ? `${revenue.fiscal_label} revenue · ended ${revenue.period_end}` : "Unavailable at selected research date"}</small><b>Explore the figures ↗</b></Link>; })}</div></section>;
}

export function CashLens({ values, company }: { values: Metric[]; company: string }) {
  const [selectedEnd, setSelectedEnd] = useState("");
  const periods = values.filter(m => m.company === company && m.metric === "revenue");
  const latest = periods.find(m => m.period_end === selectedEnd) || periods.at(-1);
  if (!latest) return <div className="notice" role="status">No annual dataset was available for this company by the selected research date.</div>;
  const get = (key: string) => values.find(m => m.company === company && m.period_end === latest.period_end && m.metric === key);
  const cash = get("operating_cash_flow_margin"), spending = get("capex_revenue"), residual = get("free_cash_flow_margin");
  return <section className="financial-cash-lens" aria-label="Selected company cash conclusion"><div className="financial-lens-heading"><span className="directory-eyebrow">{latest.fiscal_label} / ENDED {latest.period_end}</span><h2>Where does the revenue go?</h2><div className="cash-lens-periods" role="group" aria-label="Cash analysis annual period">{periods.map(m => <button key={m.period_end} aria-pressed={m.period_end === latest.period_end} onClick={() => setSelectedEnd(m.period_end)}>{m.fiscal_label}<small>Ended {m.period_end}</small></button>)}</div><p>Amounts below are per 100 units of revenue. Scope differs between companies; this is not a ranking.</p></div><div className="cash-lens-grid">{[{m:cash,label:"Operating cash generated",tone:"mint"},{m:spending,label:company === "MU" ? "Net capital investment" : "Disclosed capital investment",tone:"gold"},{m:residual,label:residual?.label || "Cash after capital outlays",tone:"blue"}].map(({m,label,tone}) => <article key={label} className={`cash-lens-card ${tone}`}><span>{label}</span><strong>{m ? Number(m.value).toFixed(2) : "—"}<small>/ 100</small></strong><div className="cash-lens-track" aria-hidden="true"><i className={m && Number(m.value)<0 ? "negative" : ""} style={{width:`${m ? Math.min(100,Math.abs(Number(m.value))) : 0}%`}}/></div><p>{m && Number(m.value)<0 ? "Negative cash residual" : "Annual revenue denominator"}</p></article>)}</div>{residual && <div className="cash-lens-definition"><p>{residual.definition}</p><MetricTrace metric={get("free_cash_flow")}/></div>}{company === "NVDA" && <p className="small-note">The cash residual also subtracts related principal payments, which are excluded from the capital-investment ratio above.</p>}</section>;
}
