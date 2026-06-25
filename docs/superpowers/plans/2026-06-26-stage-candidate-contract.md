# Stage Candidate Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Pin the public Stage-1 candidate row that later scorer stages can read without depending on private graph lookup, scorer runtime, or evidence rows.

**Architecture:** Add one frozen `StageCandidate` dataclass beside `CandidateSet` and `EvidenceSet`. It serializes the Stage-1 boundary only: candidate fingerprint, public entity ref, fused score, RRF ranks, and retrieval provenance. Do not add Stage-2 IRT fields, LLM tie-break fields, conformal shortlist fields, source adapters, graph lookup, storage, telemetry, or private tuning.

**Tech Stack:** Python stdlib dataclasses, JSON Schema draft 2020-12, TypeScript source types, stdlib `unittest`.

---

### Task 1: Core Stage Candidate Contract

**Files:**
- Modify: `tests/test_core_contracts.py`
- Modify: `tests/test_core_fixtures.py`
- Modify: `packages/core/src/evalrank_core/contracts.py`
- Modify: `packages/core/src/evalrank_core/fixtures.py`
- Modify: `packages/core/src/evalrank_core/__init__.py`

- [x] **Step 1: Write failing core and fixture tests**

Add tests that construct:

```python
StageCandidate(
    candidate_id=sample_capability_fingerprint_input().fingerprint(),
    entity=EntityRef(entity_type="mcp_server", entity_id="tool:public-search-demo"),
    fused_score=0.032786,
    rrf_components={"lexical_rank": 1, "semantic_rank": 2, "graph_rank": None},
    retrieval_arms=("lexical", "semantic"),
    use_case="web-research:freshness-check",
)
```

Assert `to_dict()` emits `object`, `candidate_id`, `entity`, `fused_score`, `rrf_components`, and `retrieval_provenance`. Assert invalid fingerprint, negative score, missing RRF keys, zero rank, duplicate arms, blank arm, and blank use case are rejected. Add a fixture test for `sample_stage_candidate()`.

- [x] **Step 2: Run red core tests**

```sh
python3 -m unittest tests.test_core_contracts tests.test_core_fixtures
```

Expected: fail because `StageCandidate` and `sample_stage_candidate()` do not exist.

- [x] **Step 3: Implement minimal core contract**

Add frozen `StageCandidate` with:

```python
class StageCandidate:
    object: ClassVar[str] = "stage_candidate"
    candidate_id: str
    entity: EntityRef
    fused_score: float
    rrf_components: dict[str, int | None]
    retrieval_arms: tuple[str, ...]
    use_case: str
```

Validate 64-character lowercase hex `candidate_id`, `EntityRef`, non-negative numeric `fused_score`, exact RRF keys `lexical_rank`, `semantic_rank`, `graph_rank`, positive integer-or-null ranks, at least one unique non-blank arm, and non-blank `use_case`. Serialize `entity` through `EntityRef.to_dict()`, sort `retrieval_arms`, and round `fused_score` with the existing `_round_score()` helper.

- [x] **Step 4: Run focused core tests**

```sh
python3 -m unittest tests.test_core_contracts tests.test_core_fixtures
```

Expected: pass.

### Task 2: Schema And SDK Mirrors

**Files:**
- Modify: `tests/test_schema_contracts.py`
- Create: `schemas/stage-candidate.schema.json`
- Modify: `schemas/README.md`
- Modify: `tests/test_sdk_python.py`
- Modify: `tests/test_sdk_ts.py`
- Modify: `packages/sdk-python/src/evalrank_sdk/__init__.py`
- Modify: `packages/sdk-ts/src/index.ts`

- [x] **Step 1: Write failing schema and SDK tests**

Require `stage-candidate.schema.json` to mirror `StageCandidate.to_dict()`, use draft 2020-12, be a closed object, and pin the exact RRF/provenance shape. Require Python and TypeScript SDK surfaces to expose `StageCandidate` and `sample_stage_candidate()`.

- [x] **Step 2: Run red schema and SDK tests**

```sh
python3 -m unittest tests.test_schema_contracts tests.test_sdk_python tests.test_sdk_ts
```

Expected: fail because the schema and SDK exports do not exist.

- [x] **Step 3: Add minimal schema and SDK exports**

Create a closed schema with required `object`, `candidate_id`, `entity`, `fused_score`, `rrf_components`, and `retrieval_provenance`. Add Python SDK re-export and TypeScript `StageCandidate` interface. Keep Stage-2+ scorer fields out.

- [x] **Step 4: Run focused schema and SDK tests**

```sh
python3 -m unittest tests.test_schema_contracts tests.test_sdk_python tests.test_sdk_ts
npm run check --prefix packages/sdk-ts
```

Expected: pass.

### Task 3: Fixture Adapters And Docs

**Files:**
- Modify: `tests/test_cli_fixture.py`
- Modify: `tests/test_mcp_fixture.py`
- Modify: `packages/cli/src/evalrank_cli/__init__.py`
- Modify: `packages/mcp/src/evalrank_mcp/__init__.py`
- Modify: `README.md`
- Modify: `TESTS.md`
- Modify: `docs/STATUS.md`
- Modify: `docs/PORTING.md`
- Modify: package READMEs as needed
- Modify: `methods/scoring-stages.md`
- Create: `docs/build-log/2026-06-26-stage-candidate-contract.md`

- [x] **Step 1: Write failing CLI and MCP tests**

Require `evalrank fixture stage-candidate` and `evalrank.fixture` with `kind="stage-candidate"` to return the deterministic public stage candidate fixture.

- [x] **Step 2: Run red CLI and MCP tests**

```sh
python3 -m unittest tests.test_cli_fixture tests.test_mcp_fixture
```

Expected: fail because `stage-candidate` is not an allowed fixture kind.

- [x] **Step 3: Add minimal fixture adapter support and docs**

Wire `sample_stage_candidate().to_dict()` into the existing CLI/MCP fixture switches and update public docs/status/porting/build-log. Keep scorer implementation, graph lookup, Stage-2+ fields, storage, telemetry, and private tuning out of scope.

- [x] **Step 4: Run full checks, review, commit, push**

```sh
make check
npm run check --prefix packages/sdk-ts
```

Expected: pass. Then run public boundary/secret scan, gstack review, Ponytail review, commit, push directly to `main`, and verify the matching CI run.

## What Already Exists

- `EntityRef` already serializes public entity identity; reuse it instead of adding another entity row.
- `CandidateSet` already lists candidate membership; `StageCandidate` only adds Stage-1 ranking metadata for one candidate.
- `CapabilityFingerprintInput.fingerprint()` already produces the candidate join key; reuse it in the fixture.
- CLI and MCP fixture switches already exist; add one branch each.

## NOT In Scope

- Stage-2 IRT/theta/trust fields: private scorer inputs are not public-safe yet.
- Stage-3 LLM tie-break fields: materialize-time behavior is runtime work, not a public contract row.
- Stage-4 conformal/diversity fields: shortlist membership belongs after scorer/runtime split.
- Graph lookup/source adapters/storage: private incubation until public-input-only pieces are separable.
- OpenAPI route changes: this row is not part of the public `POST /v1/recommendations` response yet.

## Self-Review

- Spec coverage: Covers the public Stage-1 boundary row from the build map without adding runtime scorer behavior.
- Placeholder scan: No placeholders.
- Type consistency: `StageCandidate`, `stage-candidate.schema.json`, `sample_stage_candidate`, and fixture kind `stage-candidate` are consistent.

## GSTACK REVIEW REPORT

Plan review: PASS. The plan reuses existing `EntityRef`, fingerprint, fixture, schema, SDK, CLI, and MCP patterns. No extra service, storage layer, dependency, or scorer runtime is needed.

NO UNRESOLVED DECISIONS
