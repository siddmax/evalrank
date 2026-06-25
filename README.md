# EvalRank

EvalRank is the public core for evidence-ranked evaluation primitives. This repository holds the open schemas, scoring method interfaces, SDK boundaries, examples, and CI gates that keep the core independent from any private Syndai application code.

## Repository Layout

- `AGENTS.md` - Root agent guide and evolution rules.
- `TESTS.md` - Current test commands and test map.
- `docs/STATUS.md` - Living build progress tracker.
- `docs/REPO_STRUCTURE.md` - Directory ownership map.
- `docs/PORTING.md` - Public/private porting decisions and workstream ownership.
- `NAVIGATION.md` - Public route contract entrypoints.
- `packages/core` - Python reference package for evidence, candidate, and scoring contracts.
- `packages/mcp` - MCP server boundary for evaluation and evidence lookup tools.
- `packages/cli` - Command-line entrypoints that call the public APIs.
- `packages/sdk-python` - Python SDK packaging boundary.
- `packages/sdk-ts` - TypeScript SDK packaging boundary.
- `methods` - Public method notes and implementation boundaries.
- `schemas` - Public JSON schema contracts.
- `examples` - Minimal runnable examples.

## What Is Not Open

The hosted product, private Syndai application integrations, private benchmark fixtures, held-out eval data, production telemetry, customer data, and proprietary ranking experiments are not part of this repository. Public packages must not import private Syndai namespaces or depend on private services.

Use `docs/PORTING.md` before moving any private work into this repo.

## Database Boundary

During incubation, EvalRank uses the existing Finn/Supabase project with a private `evalrank` schema. The schema migrations and live DB bootstrap are kept in the Syndai repo because Syndai currently owns the shared Finn/Supabase deploy path and guardrails.

Move database migrations into this repo only when EvalRank owns its own deploy/release path or moves to its own Supabase project. When that happens, update `AGENTS.md`, `TESTS.md`, and this README in the same change.

## Boundary Contract

Run:

```sh
make check
```

The boundary gate rejects private imports, Smithery coupling, Min-K% implementation markers, secret files, high-signal secret values, private data paths, and public packages missing license or notice files.

## Public API Contract

The public route contracts live in `schemas/openapi.json`.

- `GET /v1/use-cases` returns the storage-free `UseCaseCatalog` taxonomy contract.
- `GET /v1/scoring-stages` returns the storage-free `ScoringStageCatalog` method-stage contract.
- `POST /v1/recommendations` accepts `EvaluationRequest` JSON, returns `Recommendation` JSON, and uses RFC 9457 `application/problem+json` for malformed payloads, validation errors, rate limits, temporary unavailability, and upstream timeouts.

The public error contract includes optional retry fields and reusable `Retry-After`, `RateLimit`, and `RateLimit-Policy` header definitions. This is a contract only. Hosted auth, scorer runtime, benchmark weights, rate-limit enforcement, persistence, receipt IDs, private problem types, and deployment wiring stay outside this public repo.

## Public Fixture Surfaces

These examples use local checkout paths until the packages are published.

Runnable example:

```sh
python3 examples/public_fixture.py
```

The example prints the current synthetic public fixture bundle: raw entry, request, candidate set, stage candidate, evidence item, evidence set, result row, use-case catalog, scoring stage catalog, exclusion, and recommendation.

CLI:

```sh
PYTHONPATH=packages/core/src:packages/cli/src python3 -m evalrank_cli fixture fingerprint
PYTHONPATH=packages/core/src:packages/cli/src python3 -m evalrank_cli fixture raw-entry
PYTHONPATH=packages/core/src:packages/cli/src python3 -m evalrank_cli fixture request
PYTHONPATH=packages/core/src:packages/cli/src python3 -m evalrank_cli fixture candidate-set
PYTHONPATH=packages/core/src:packages/cli/src python3 -m evalrank_cli fixture stage-candidate
PYTHONPATH=packages/core/src:packages/cli/src python3 -m evalrank_cli fixture evidence
PYTHONPATH=packages/core/src:packages/cli/src python3 -m evalrank_cli fixture result-row
PYTHONPATH=packages/core/src:packages/cli/src python3 -m evalrank_cli fixture ranking-group
PYTHONPATH=packages/core/src:packages/cli/src python3 -m evalrank_cli fixture evidence-set
PYTHONPATH=packages/core/src:packages/cli/src python3 -m evalrank_cli fixture exclusion
PYTHONPATH=packages/core/src:packages/cli/src python3 -m evalrank_cli fixture use-cases
PYTHONPATH=packages/core/src:packages/cli/src python3 -m evalrank_cli fixture scoring-stages
PYTHONPATH=packages/core/src:packages/cli/src python3 -m evalrank_cli fixture recommendation
```

Python SDK:

```python
from evalrank_sdk import sample_candidate_set, sample_evidence_set, sample_exclusion, sample_ranking_group, sample_recommendation, sample_result_row, sample_scoring_stage_catalog, sample_stage_candidate, sample_use_case_catalog

use_cases = sample_use_case_catalog().to_dict()
stages = sample_scoring_stage_catalog().to_dict()
candidate_set = sample_candidate_set().to_dict()
stage_candidate = sample_stage_candidate().to_dict()
result_row = sample_result_row().to_dict()
ranking_group = sample_ranking_group().to_dict()
evidence_set = sample_evidence_set().to_dict()
exclusion = sample_exclusion().to_dict()
payload = sample_recommendation().to_dict()
call = payload["the_call"]
```

MCP adapter:

```python
from evalrank_mcp import call_tool

result = call_tool("evalrank.fixture", {"kind": "fingerprint"})
```

TypeScript SDK:

```ts
import { type CandidateSet, type EvidenceSet, type Exclusion, type ProblemDetails, type RankingGroup, type ResultRow, type ScoringStageCatalog, type StageCandidate, type TheCall, type UseCaseCatalog } from "@evalrank/sdk";

const useCases: UseCaseCatalog["use_cases"] = [];
const stages: ScoringStageCatalog["stages"] = [];
const candidates: CandidateSet["candidates"] = [{ entity_type: "mcp_server", id: "tool:public-search-demo" }];
const arms: StageCandidate["retrieval_provenance"]["arms"] = ["lexical", "semantic"];
const verification: ResultRow["verification_state"] = "verified";
const grouped: RankingGroup["ranked"] = [];
const evidence: EvidenceSet["evidence_items"] = [];
const exclusion: Exclusion["reason"] = "unknown_cost";
const call: TheCall["decision"] = "recommend";
const problem: ProblemDetails["code"] = "rate_limited";
```
