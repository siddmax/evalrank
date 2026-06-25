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

export type TrustTier = (typeof TRUST_TIERS)[number];
export type FreshnessStatus = (typeof FRESHNESS_STATUSES)[number];
export type ComparabilityMode = (typeof COMPARABILITY_MODES)[number];
export type EvidenceKind = (typeof EVIDENCE_KINDS)[number];

export interface Freshness {
  last_eval: string;
  next_refresh: string;
  status: FreshnessStatus;
}

export interface EntityRef {
  entity_type: string;
  id: string;
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
  the_call: Record<string, unknown> | null;
  exclusions: Record<string, unknown>[];
  recommendation_id: string;
  recommend_id: string;
  search_run_id: string;
  request_id: string;
}
