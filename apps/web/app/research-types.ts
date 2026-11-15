export type Metric = { label?: string; company: string; currency: string; unit_scale: number; accounting_basis: string; metric: string; value: string; unit: string; period_end: string; fiscal_label: string; definition: string; classification: string; inputs: { fact_id: string; currency: string; unit_scale: number; source_title: string; source_id: string; url: string; locator: string; value: string; metric: string; published_at: string }[] };
export type Source = { publication_date?: string; id: string; title: string; company: string; publisher: string; url: string; published_at: string; retrieved_at: string; checksum: string; capture_kind: string; accounting_basis: string };
export type Company = { ticker: string; name: string; role: string; layer: string; coverage: string; url: string };
export type Evaluation = { executed: boolean; passed?: number; total?: number; kind?: string; human_reviewed?: boolean; note?: string };
export type Snapshot = { generated_at: string; research_as_of: string; sources: Source[]; metrics: Metric[]; companies: Company[]; definitions: Record<string, string>; limitations: string[]; evaluation: Evaluation; investigation: Investigation; directory: Directory; applications: ApplicationCatalog };
export type Evidence = { citation_id: number; source_id: string; title: string; text: string; locator: string; url: string; published_at: string; period_end?: string };
export type Answer = { mode: string; abstained: boolean; paragraphs: { text: string; citations: number[]; classification: string }[]; evidence: Evidence[]; citation_support: string; latency_ms?: number; limitation?: string; as_of: string; model_calls: number };

export type Investigation = { id: string; as_of: string; human_reviewed: boolean; historical_archive_certified: boolean; comparability: Record<string, string>; periods: { window: string; company: string; period_end: string; metrics: Metric[]; missing: { metric: string; reason: string }[] }[] };

export type DirectoryCategory = { id: string; label: string; description: string; color: string };
export type DirectoryCompany = { id: string; name: string; roles: string[]; focus: string; website: string; investor_url: string | null; financial_company_id: "NVDA" | "TSM" | "ASML" | "MU" | "TXN" | "AMKR" | null; financial_loaded: boolean };
export type ResearchResource = { id: string; title: string; publisher: string; category: string; url: string; description: string; access: "public" | "mixed"; roles: string[] };
export type Directory = { version: string; catalog_date: string; scope: string; financial_coverage_note: string; categories: DirectoryCategory[]; resource_categories: { id: string; label: string }[]; companies: DirectoryCompany[]; resources: ResearchResource[]; link_observations: { url: string; state: string; status: number | null; checked_at: string }[] };

export type ChipFunctionId = "compute" | "sense" | "communicate" | "control" | "power";
export type ApplicationSceneId = "ai" | "car" | "city" | "robot" | "plane" | "design" | "energy" | "health" | "connected";
export type ChipFunction = { id: ChipFunctionId; label: string; description: string; color: string };
export type ApplicationReference = { id: string; publisher: string; title: string; url: string; reviewed_on: string; support: string; company_id: string|null; publication_date: string|null; link_status: number|null; link_checked_on: string|null; access_note: string|null };
export type ApplicationStep = { id: string; label: string; task: string; functions: ChipFunctionId[]; chips: string[]; explanation: string; company_ids: string[]; source_ids: string[]; economic_question: string };
export type ApplicationWorld = { id: string; label: string; short_label: string; scene: ApplicationSceneId; color: string; summary: string; functions: ChipFunctionId[]; source_ids: string[]; depth: "guided_story"|"overview"; steps: ApplicationStep[] };
export type ApplicationCatalog = { version: string; reviewed_on: string; human_reviewed: false; scope: string; functions: ChipFunction[]; sources: ApplicationReference[]; worlds: ApplicationWorld[]; footprints: { id:string;region:string;location:string;role:string;company_id:string;description:string;source_ids:string[] }[] };
