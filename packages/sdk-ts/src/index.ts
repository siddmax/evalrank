export const TRUST_TIERS = [
  "verified",
  "standardized",
  "self-reported",
  "tracking-only",
] as const;

export const FRESHNESS_STATUSES = [
  "fresh",
  "stale",
  "recalibrating",
] as const;

export const COMPARABILITY_MODES = [
  "single-scale",
  "kind-grouped",
] as const;

export const EVIDENCE_KINDS = [
  "attestation",
  "benchmark",
  "documentation",
  "runtime-observation",
  "trace",
] as const;

export const RESULT_ENTITY_KINDS = [
  "model",
  "tool_server",
  "agent",
] as const;

export const RESULT_VERIFICATION_STATES = [
  "verified",
  "provisional",
] as const;

export const RESULT_FLAG_KEYS = [
  "saturated",
  "contaminated",
  "judge_model_dependent",
  "scaffold_nonstandard",
] as const;

export const THE_CALL_DECISIONS = [
  "abstain",
  "recommend",
] as const;

export const PROBLEM_CODES = [
  "rate_limited",
  "upstream_timeout",
  "validation",
  "not_found",
  "methodology_stale",
  "internal",
  "unauthorized",
  "forbidden",
] as const;

export type TrustTier = (typeof TRUST_TIERS)[number];
export type FreshnessStatus = (typeof FRESHNESS_STATUSES)[number];
export type ComparabilityMode = (typeof COMPARABILITY_MODES)[number];
export type EvidenceKind = (typeof EVIDENCE_KINDS)[number];
export type ResultEntityKind = (typeof RESULT_ENTITY_KINDS)[number];
export type ResultVerificationState = (typeof RESULT_VERIFICATION_STATES)[number];
export type TheCallDecision = (typeof THE_CALL_DECISIONS)[number];
export type ProblemCode = (typeof PROBLEM_CODES)[number];

export interface Freshness {
  last_eval: string;
  next_refresh: string;
  status: FreshnessStatus;
}

export interface EntityRef {
  entity_type: string;
  id: string;
}

export interface Exclusion {
  subject: EntityRef;
  reason: string;
  detail: string;
}

export interface CapabilityFingerprint {
  object: "capability_fingerprint";
  id_scheme: string;
  canonical_id: string;
  entity_kind: string;
  declared_capability_shape: Record<string, unknown>;
  capability_fingerprint: string;
}

export interface EvaluationRequest {
  object: "evaluation_request";
  request_id: string;
  use_case: string;
  entity_types: string[];
  requested_at: string;
  constraints: Record<string, unknown>;
}

export interface CandidateSet {
  object: "candidate_set";
  request_id: string;
  use_case: string;
  candidates: EntityRef[];
  generated_at: string;
}

export interface StageCandidate {
  object: "stage_candidate";
  candidate_id: string;
  entity: EntityRef;
  fused_score: number;
  rrf_components: {
    lexical_rank: number | null;
    semantic_rank: number | null;
    graph_rank: number | null;
  };
  retrieval_provenance: {
    arms: string[];
    use_case: string;
  };
}

export interface EvidenceSet {
  object: "evidence_set";
  request_id: string;
  use_case: string;
  evidence_items: EvidenceItem[];
  generated_at: string;
}

export interface RawEntry {
  object: "raw_entry";
  source: string;
  source_id: string;
  entity_kind: string;
  canonical_id: string;
  raw_metadata: Record<string, unknown>;
  declared_capability_shape: Record<string, unknown>;
  fetched_at: string;
  content_hash: string;
}

export interface EvidenceItem {
  evidence_id: string;
  subject: EntityRef;
  kind: EvidenceKind;
  source: string;
  observed_at: string;
  summary: string;
  score: number | null;
  metadata: Record<string, unknown>;
}

export interface ResultRow {
  object: "result_row";
  entity_id: string;
  entity_kind: ResultEntityKind;
  benchmark_id: string;
  benchmark_version: string;
  harness: string;
  harness_version: string;
  is_self_reported: boolean;
  n_items: number;
  ci95: [number, number];
  score_raw: number;
  score_unit: string;
  date_run: string;
  model_version: string;
  provenance: Record<string, unknown>;
  source_url: string;
  attribution_string: string;
  flags: {
    saturated: boolean;
    contaminated: boolean;
    judge_model_dependent: boolean;
    scaffold_nonstandard: boolean;
  };
  verification_state: ResultVerificationState;
}

export interface TheCall {
  decision: TheCallDecision;
  confidence: number | null;
  reason: string;
  abstention_reason: string | null;
}

export interface ProblemDetails {
  type: string;
  title: string;
  status: number;
  detail: string;
  instance?: string;
  code?: ProblemCode;
  retriable?: boolean;
  retry_after?: number;
  field?: string;
  request_id?: string;
  doc_url?: string;
  [key: string]: unknown;
}

export interface RankedEntity {
  entity_type: string;
  id: string;
  rank: number;
  capability_score: number;
  confidence: number;
  ci95: [number, number];
  methodology_version: string;
  trust_tier: TrustTier;
  score_components: Record<string, number>;
  axes: Record<string, unknown>;
  freshness: Freshness;
  caveats: string[];
}

export interface Recommendation {
  object: "recommendation";
  use_case: string;
  shortlist_depth: number;
  depth_rationale: string;
  degraded: boolean;
  served_from: string;
  base_snapshot_lag_ms: number;
  methodology_version: string;
  generated_at: string;
  comparability: ComparabilityMode;
  ranked: RankedEntity[];
  groups: Record<string, unknown>[] | null;
  the_call: TheCall | null;
  exclusions: Exclusion[];
  recommendation_id: string;
  recommend_id: string;
  search_run_id: string;
  request_id: string;
}
