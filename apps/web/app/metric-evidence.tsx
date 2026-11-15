"use client";

import { ArrowUpRight, ExternalLink } from "lucide-react";
import type { Metric } from "./research-types";

const labels: Record<string, string> = { revenue: "Revenue", revenue_growth: "Revenue growth", gross_margin: "Gross margin", operating_margin: "Operating margin", operating_cash_flow: "Operating cash flow", operating_cash_flow_margin: "Operating cash / revenue", capex_revenue: "Disclosed capital spending / revenue", capex_operating_cash_flow: "Capital spending / operating cash", free_cash_flow: "Cash after disclosed capital outlays", free_cash_flow_margin: "Cash remaining / revenue", capital_asset_sales: "PPE sale proceeds", capital_grants: "Government incentives", capital_purchases: "Capital purchases (source scope)", capital_principal: "Related principal payments", capital_expenditures: "Annual-report capital expenditures" };
export const metricLabel = (key: string) => labels[key] || key.replaceAll("_", " ");
export function formatMetric(metric?: Metric) {
  if (!metric) return "Unavailable";
  if (metric.unit === "%") return `${Number(metric.value).toFixed(2)}%`;
  const scale = metric.unit_scale || (metric.unit.includes("thousand") ? 1000 : 1000000);
  return `${metric.currency === "TWD" ? "NT$" : metric.currency === "EUR" ? "€" : "US$"}${(Number(metric.value) * scale / 1e9).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}B`;
}

export function MetricTrace({ metric }: { metric?: Metric }) {
  if (!metric) return <span className="missing-metric">Unavailable at this research date</span>;
  return <details className="metric-trace"><summary>Inspect calculation & source rows <ArrowUpRight size={12}/></summary><p>{metric.definition}</p><p className="small-note">{metric.fiscal_label} · ended {metric.period_end} · {metric.accounting_basis}<br/>Result in original units: {metric.value} {metric.unit}</p><ul>{metric.inputs.map((input, i) => <li key={`${input.fact_id || input.source_id}-${i}`}><strong>{metricLabel(input.metric)}: {Number(input.value).toLocaleString("en-US", { maximumFractionDigits: 8 })} {input.currency || metric.currency} {input.unit_scale === 1000 ? "thousand" : "million"}</strong><span>{input.locator}</span><a href={`${input.url}${input.url.endsWith(".pdf") ? `#page=${input.locator.match(/PDF p\. (\d+)/)?.[1] || 1}` : ""}`} target="_blank" rel="noreferrer">{input.source_title || "Original financial table"} <ExternalLink size={11}/></a></li>)}</ul><p className="small-note">Calculated with Decimal from stored source rows. Display values are rounded. Citation support still needs independent human review.</p></details>;
}
