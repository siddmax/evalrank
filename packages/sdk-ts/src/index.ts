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

export const USE_CASE_ENTITY_KINDS = [
  "agent",
  "model",
  "tool",
] as const;

export const USE_CASE_RANK_POLICIES = [
  "ranked",
  "veto_overlay",
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

export const PUBLIC_FIXTURE_KINDS = [
  "candidate-set",
  "evidence",
  "evidence-set",
  "exclusion",
  "fingerprint",
  "problem",
  "raw-entry",
  "recommendation",
  "ranking-group",
  "result-row",
  "request",
  "scoring-stages",
  "stage-candidate",
  "use-cases",
] as const;

export type TrustTier = (typeof TRUST_TIERS)[number];
export type FreshnessStatus = (typeof FRESHNESS_STATUSES)[number];
export type ComparabilityMode = (typeof COMPARABILITY_MODES)[number];
export type EvidenceKind = (typeof EVIDENCE_KINDS)[number];
export type ResultEntityKind = (typeof RESULT_ENTITY_KINDS)[number];
export type ResultVerificationState = (typeof RESULT_VERIFICATION_STATES)[number];
export type TheCallDecision = (typeof THE_CALL_DECISIONS)[number];
export type UseCaseEntityKind = (typeof USE_CASE_ENTITY_KINDS)[number];
export type UseCaseRankPolicy = (typeof USE_CASE_RANK_POLICIES)[number];
export type ProblemCode = (typeof PROBLEM_CODES)[number];
export type PublicFixtureKind = (typeof PUBLIC_FIXTURE_KINDS)[number];
export type NonEmptyArray<T> = [T, ...T[]];

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

export interface Abstention {
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
  entity_types: NonEmptyArray<string>;
  requested_at: string;
  constraints: Record<string, unknown>;
}

export interface CandidateSet {
  object: "candidate_set";
  request_id: string;
  use_case: string;
  candidates: NonEmptyArray<EntityRef>;
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
    arms: NonEmptyArray<string>;
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

export interface UseCaseBase {
  object: "use_case";
  id: string;
  name: string;
  definition: string;
  entity_kinds: NonEmptyArray<UseCaseEntityKind>;
}

export interface RankedUseCase extends UseCaseBase {
  rank_policy: "ranked";
  is_overlay: false;
}

export interface OverlayUseCase extends UseCaseBase {
  rank_policy: "veto_overlay";
  is_overlay: true;
}

export type UseCase = RankedUseCase | OverlayUseCase;

export interface UseCaseCatalog {
  object: "use_case_catalog";
  methodology_version: string;
  generated_at: string;
  use_cases: NonEmptyArray<UseCase>;
}

export interface ScoringStage {
  id: string;
  ordinal: number;
  name: string;
  description: string;
  input_contracts: NonEmptyArray<string>;
  output_contracts: NonEmptyArray<string>;
  public_boundary: string;
}

export interface ScoringStageCatalog {
  object: "scoring_stage_catalog";
  methodology_version: string;
  generated_at: string;
  stages: NonEmptyArray<ScoringStage>;
}

export interface RecommendCall {
  decision: "recommend";
  confidence: number;
  reason: string;
  abstention_reason: null;
}

export interface AbstainCall {
  decision: "abstain";
  confidence: null;
  reason: string;
  abstention_reason: string;
}

export type TheCall = RecommendCall | AbstainCall;

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
  axes: {
    evidence: {
      n_items: number;
      coverage: TrustTier;
    };
  };
  freshness: Freshness;
  caveats: string[];
}

export interface RankingGroup {
  object: "ranking_group";
  group_key: string;
  entity_type: string;
  ranked: NonEmptyArray<RankedEntity>;
  group_rationale: string;
}

export interface RecommendationBase {
  object: "recommendation";
  use_case: string;
  shortlist_depth: number;
  depth_rationale: string;
  degraded: boolean;
  served_from: string;
  base_snapshot_lag_ms: number;
  methodology_version: string;
  generated_at: string;
  exclusions: Exclusion[];
  recommendation_id: string;
  recommend_id: string;
  search_run_id: string;
  request_id: string;
}

export interface RecommendationWithoutCall {
  the_call: null;
  abstention: null;
}

export interface RecommendationWithRecommendCall {
  the_call: RecommendCall;
  abstention: null;
}

export interface RecommendationWithAbstainCall {
  the_call: AbstainCall;
  abstention: Abstention;
}

export type RecommendationCallState =
  | RecommendationWithoutCall
  | RecommendationWithRecommendCall
  | RecommendationWithAbstainCall;

export interface SingleScaleRecommendationBase extends RecommendationBase {
  comparability: "single-scale";
  ranked: RankedEntity[];
  groups: null;
}

export interface KindGroupedRecommendationBase extends RecommendationBase {
  comparability: "kind-grouped";
  ranked: [];
  groups: NonEmptyArray<RankingGroup>;
}

export interface EmptySingleScaleAbstentionRecommendation
  extends RecommendationBase,
    RecommendationWithAbstainCall {
  comparability: "single-scale";
  shortlist_depth: 0;
  ranked: [];
  groups: null;
}

export type SingleScaleRecommendation =
  | (SingleScaleRecommendationBase & (RecommendationWithoutCall | RecommendationWithRecommendCall))
  | EmptySingleScaleAbstentionRecommendation;
export type KindGroupedRecommendation = KindGroupedRecommendationBase &
  (RecommendationWithoutCall | RecommendationWithRecommendCall);
export type Recommendation = SingleScaleRecommendation | KindGroupedRecommendation;

export class EvalRankApiError extends Error {
  readonly status: number;
  readonly problem: ProblemDetails;
  readonly retryAfter: number | null;

  constructor(status: number, problem: ProblemDetails, retryAfter: number | null = null) {
    super(`EvalRank API error ${status}: ${problem.title ?? "request failed"}`);
    this.name = "EvalRankApiError";
    this.status = status;
    this.problem = problem;
    this.retryAfter = retryAfter;
  }
}

export class EvalRankClient {
  readonly baseUrl: string;

  constructor(baseUrl: string) {
    const parsed = new URL(baseUrl);
    if (!["http:", "https:"].includes(parsed.protocol) || !parsed.host) {
      throw new TypeError("baseUrl must be an http or https URL");
    }
    this.baseUrl = baseUrl.replace(/\/+$/, "");
  }

  async useCases(): Promise<UseCaseCatalog> {
    return this.requestJson<UseCaseCatalog>("/v1/use-cases");
  }

  async scoringStages(): Promise<ScoringStageCatalog> {
    return this.requestJson<ScoringStageCatalog>("/v1/scoring-stages");
  }

  async recommend(request: EvaluationRequest): Promise<Recommendation> {
    return this.requestJson<Recommendation>("/v1/recommendations", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    });
  }

  private async requestJson<T>(
    path: string,
    init: RequestInit = {},
  ): Promise<T> {
    const response = await fetch(`${this.baseUrl}${path}`, {
      ...init,
      headers: {
        Accept: "application/json",
        ...init.headers,
      },
    });
    const body = await response.json();
    if (!response.ok) {
      throw new EvalRankApiError(response.status, body as ProblemDetails, retryAfter(response.headers));
    }
    return body as T;
  }
}

function retryAfter(headers: Headers): number | null {
  const value = headers.get("Retry-After");
  if (value === null) {
    return null;
  }
  const trimmed = value.trim();
  if (!/^\d+$/.test(trimmed)) {
    return null;
  }
  const parsed = Number.parseInt(trimmed, 10);
  return Number.isSafeInteger(parsed) ? parsed : null;
}
