"use client";
import { useEffect, useRef, useState } from "react";
import type { Data, Layout } from "plotly.js";

type Observation = { year: string; value: number };
const format = (value: number, percent: boolean, currency = "USD") => percent ? `${value.toFixed(2)}%` : `${currency === "TWD" ? "NT$" : currency === "EUR" ? "€" : "$"}${value.toFixed(2)}B`;

export default function FinancialChart({ data, label, percent = false, currency = "USD" }: { data: Observation[]; label: string; percent?: boolean; currency?: string }) {
  const ref = useRef<HTMLDivElement>(null);
  const [view, setView] = useState<"columns" | "slope">("columns");
  useEffect(() => {
    let stopped = false;
    const element = ref.current;
    async function render() {
      const [{ default: Plotly }] = await Promise.all([import("plotly.js-basic-dist-min"), document.fonts.ready]);
      if (stopped || !element) return;
      const theme = getComputedStyle(element);
      const colour = (token: string) => theme.getPropertyValue(token).trim();
      const colours = data.map((_, i) => colour(i === data.length - 1 ? "--chart-current" : "--chart-previous"));
      const years = data.map(d => d.year);
      const values = data.map(d => d.value);
      const text = data.map(d => format(d.value, percent, currency));
      const common = { hovertemplate: percent ? "%{y}<br>%{x:,.2f}% of revenue<extra></extra>" : `%{x}<br>%{y:,.2f} ${currency} billion<extra></extra>` };
      let traces: Data[];
      if (percent) {
        traces = [
          { type: "bar", orientation: "h", y: years, x: data.map(() => 100), marker: { color: colour("--chart-track") }, width: .3, hoverinfo: "skip" },
          { type: "bar", orientation: "h", y: years, x: values, width: .3, marker: { color: colours, pattern: { shape: data.map((_, i) => i === data.length-1 ? "" : "/"), solidity: .12, fgcolor: colour("--panel") } }, ...common },
          { type: "scatter", mode: "text+markers", y: years, x: values, marker: { color: colours, size: 11, line: { color: colour("--panel"), width: 3 } }, text, textposition: "top left", textfont: { size: 19, color: colour("--text") }, cliponaxis: false, ...common },
        ];
      } else if (view === "slope") {
        traces = [{ type: "scatter", mode: "text+lines+markers", x: years, y: values, line: { color: colour("--chart-current"), width: 3 }, marker: { color: colours, size: 15, line: { color: colour("--panel"), width: 4 } }, text, textposition: "top center", textfont: { size: 19, color: colour("--text") }, cliponaxis: false, ...common }];
      } else {
        traces = [
          { type: "bar", x: years, y: values, width: .4, marker: { color: colours, line: { color: colours, width: 1 }, pattern: { shape: data.map((_, i) => i === data.length-1 ? "" : "/"), solidity: .12, fgcolor: colour("--panel") } }, text, textposition: "outside", textfont: { size: 19, color: colour("--text") }, cliponaxis: false, ...common },
        ];
      }
      const layout: Partial<Layout> = {
        paper_bgcolor: "transparent", plot_bgcolor: "transparent", showlegend: false, barmode: "overlay",
        font: { family: theme.fontFamily, size: 12, color: colour("--muted") },
        hoverlabel: { bgcolor: colour("--panel"), bordercolor: colour("--accent"), font: { color: colour("--text"), family: theme.fontFamily } },
        height: 290, margin: { t: 34, l: percent ? 65 : 48, r: 24, b: 35 },
        xaxis: percent ? { range: [Math.min(0,...values)*1.25, Math.max(100,...values)*1.1], fixedrange: true, gridcolor: colour("--chart-grid"), ticksuffix: "%", dtick: 25, zeroline: true, zerolinecolor: colour("--muted") } : { type: "category", range: [-.5, Math.max(data.length-.5,.5)], fixedrange: true, showgrid: false, zeroline: false },
        yaxis: percent ? { type: "category", autorange: "reversed", fixedrange: true, showgrid: false, zeroline: false } : { range: [Math.min(0,...values)*1.3, Math.max(1, ...values)*1.3], fixedrange: true, gridcolor: colour("--chart-grid"), tickprefix: currency === "TWD" ? "NT$" : currency === "EUR" ? "€" : "$", zeroline: false, nticks: 4 },
      };
      await Plotly.newPlot(element, traces, layout, { displayModeBar: false, responsive: true });
    }
    void render();
    return () => { stopped = true; if (element) import("plotly.js-basic-dist-min").then(({ default: Plotly }) => Plotly.purge(element)); };
  }, [data, percent, view, currency]);
  return <figure className="financial-figure" aria-label={label}>
    <div className="chart-view-bar">{percent ? <span>SHARE OF REVENUE / NEGATIVE VALUES PRESERVED</span> : <><span>TWO ANNUAL OBSERVATIONS</span><div className="chart-view-toggle" aria-label="Revenue chart view"><button onClick={() => setView("columns")} aria-pressed={view === "columns"}>Columns</button><button onClick={() => setView("slope")} aria-pressed={view === "slope"}>Slope</button></div></>}</div>
    <div ref={ref} role="img" aria-label={`${label}; ${percent ? "share bars" : view} view`} className="plot"/>
    <figcaption className="chart-data-key">{data.length ? data.map((d, i) => <span key={d.year} className={i === data.length-1 ? "current" : "previous"}><i aria-hidden="true"/>{d.year}<strong>{format(d.value, percent, currency)}</strong></span>) : <span>No observations available as of this date.</span>}</figcaption>
    {!percent && view === "slope" && <p className="chart-scope-note">The line connects two annual observations; no interim values are supplied.</p>}
  </figure>;
}
