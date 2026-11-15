"use client";
import { useEffect, useRef } from "react";
import type { Data, Layout } from "plotly.js";

export default function FinancialChart({ data, label, percent = false }: { data: { year: string; value: number }[]; label: string; percent?: boolean }) {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    let stopped = false;
    const element = ref.current;
    import("plotly.js-basic-dist-min").then(({ default: Plotly }) => {
      if (stopped || !element) return;
      const traces: Data[] = [{ x: data.map(d => d.year), y: data.map(d => d.value), type: "bar", marker: { color: ["#394d57", "#b6ec9a"], line: { width: 0 } }, width: 0.46,
        hovertemplate: `%{x}<br>%{y:,.2f}${percent ? "%" : " USD billion"}<extra></extra>` }];
      const layout: Partial<Layout> = { paper_bgcolor: "transparent", plot_bgcolor: "transparent", font: { family: "Arial, sans-serif", size: 12, color: "#8d9ba1" },
        margin: { t: 26, l: 54, r: 10, b: 32 }, height: 230, xaxis: { fixedrange: true, showgrid: false, zeroline: false },
        yaxis: { fixedrange: true, gridcolor: "#253138", zeroline: false, ticksuffix: percent ? "%" : "", tickprefix: percent ? "" : "$" }, showlegend: false };
      Plotly.newPlot(element, traces, layout, { displayModeBar: false, responsive: true, staticPlot: false });
    });
    return () => { stopped = true; if (element) import("plotly.js-basic-dist-min").then(({ default: Plotly }) => Plotly.purge(element)); };
  }, [data, percent]);
  return <div ref={ref} role="img" aria-label={label} className="plot" />;
}
