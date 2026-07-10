import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";
import Ajv2020 from "ajv/dist/2020.js";

import {
  canonicalJson,
  evaluatedConfigurationId,
  isEvaluationToOfferLinkEligible,
  isServingOfferDecisionEligible,
  parseServingOfferV1,
  parseConfigurationPassportV1,
  parseDecisionQueryV1,
  parseDecisionReceiptV1,
  parseObservationV1,
  parseRunProvenanceV1,
  parseSnapshotSetDescriptorV1,
  receiptId,
  RESOLVED_IDENTITY_TRIPLES,
  sha256Hex,
  snapshotSetId,
  sourceArtifactId,
  verifyCompareResultSemantics,
  verifyEntityDetailSemantics,
  verifyLeaderboardSemantics,
  verifyLeaderboardSnapshotSet,
} from "./decision-contracts.ts";


const golden = JSON.parse(
  readFileSync(new URL("../../../examples/decision-contract-v1.golden.json", import.meta.url), "utf8"),
) as {
  utf16_set_order: { input: string[]; canonical: string[] };
  query: { input: Record<string, unknown>; canonical: string };
  receipt: { body: Record<string, unknown>; body_sha256: string; receipt_id: string };
  rejection_vectors: Array<{ name: string; value: unknown }>;
};
const manifest = JSON.parse(
  readFileSync(new URL("../../../catalog/manifest.json", import.meta.url), "utf8"),
) as {
  cells: Array<{ cell_id: string }>;
  ranking_groups: Array<{ ranking_group_id: string; entity_kind: string; interaction_policy: string; configuration_passport_class: string }>;
  benchmark_families: Array<{ benchmark_family_id: string }>;
  feeds: Array<{ feed_id: string; benchmark_family_id: string }>;
};

test("restricted JCS matches the cross-language golden bytes", async () => {
  assert.equal(canonicalJson(golden.query.input), golden.query.canonical);
  assert.equal(await sha256Hex(golden.receipt.body), golden.receipt.body_sha256);
  assert.equal(await receiptId(golden.receipt.body), golden.receipt.receipt_id);
  for (const vector of golden.rejection_vectors.slice(0, 2)) {
    assert.throws(() => canonicalJson(vector.value), /float|safe integer/);
  }
  const nullFilter = golden.rejection_vectors.find((row) => row.name === "null_provider_filter")!;
  assert.throws(() => parseDecisionQueryV1(nullFilter.value), /must not be null/);
});

test("restricted JCS orders by UTF-16 and rejects unsafe hash material", () => {
  assert.equal(canonicalJson({ "\ue000": 2, "\u{10000}": 1 }), '{"\u{10000}":1,"\ue000":2}');
  for (const value of [1.5, Number.NaN, Number.POSITIVE_INFINITY, Number.MAX_SAFE_INTEGER + 1]) {
    assert.throws(() => canonicalJson(value), /float|safe integer|finite/);
  }
  assert.throws(() => canonicalJson({ value: "\ud800" }), /surrogate/);
  assert.throws(() => canonicalJson(Array(1)), /sparse array hole/);
  assert.deepEqual(
    parseDecisionQueryV1({ ...golden.query.input, provider_ids: golden.utf16_set_order.input }).provider_ids,
    golden.utf16_set_order.canonical,
  );
});

test("content-addressed artifact and evaluated configuration identities match Python", async () => {
  const artifactHash = "a".repeat(64);
  assert.equal(sourceArtifactId(artifactHash), `artifact_${artifactHash}`);

  const rawPassport = {
    object: "configuration_passport",
    schema_version: "1",
    entity_kind: "model_configuration",
    canonical_name: "public-demo-model",
    revision: "2026-07-01",
    interaction_policy: "direct_prompt",
    configuration_passport_class: "model-configuration-v1",
    harness: null,
    scaffold: null,
    tools: ["web", "code"],
    quantization: null,
    system_prompt_policy: "benchmark-default",
    environment: "public-sandbox-v1",
  };
  const passport = parseConfigurationPassportV1(rawPassport);
  assert.equal(await evaluatedConfigurationId(passport), `config_${await sha256Hex(passport)}`);
  assert.equal(await evaluatedConfigurationId(rawPassport), await evaluatedConfigurationId(passport));
});

test("agent passports require the exact identity triple, harness, and scaffold", () => {
  const agent = {
    object: "configuration_passport",
    schema_version: "1",
    entity_kind: "agent_system",
    canonical_name: "public-agent",
    revision: "1",
    interaction_policy: "agentic",
    configuration_passport_class: "agent-system-v1",
    harness: "harness-v1",
    scaffold: "scaffold-v1",
    tools: ["shell", "browser"],
    quantization: null,
    system_prompt_policy: null,
    environment: "sandbox-v1",
  };
  assert.deepEqual(parseConfigurationPassportV1(agent).tools, ["browser", "shell"]);
  assert.throws(() => parseConfigurationPassportV1({ ...agent, harness: null }), /harness/);
  assert.throws(
    () => parseConfigurationPassportV1({ ...agent, interaction_policy: "direct_prompt" }),
    /identity triple/,
  );
});

test("identity triples and example identifiers resolve from the canonical manifest", () => {
  const manifestTriples = [...new Set(
    manifest.ranking_groups
      .filter((row) => row.entity_kind !== "unresolved")
      .map((row) => [row.entity_kind, row.interaction_policy, row.configuration_passport_class].join("|")),
  )].sort();
  assert.deepEqual(RESOLVED_IDENTITY_TRIPLES.map((row) => row.join("|")).sort(), manifestTriples);
  assert.ok(manifest.cells.some((row) => row.cell_id === golden.query.input.cell_id));
  assert.ok(manifest.ranking_groups.some((row) => row.ranking_group_id === golden.query.input.ranking_group_id));
  assert.ok(manifest.benchmark_families.some((row) => row.benchmark_family_id === "livecodebench"));
  assert.ok(manifest.feeds.some((row) => row.feed_id === "livecodebench-discovery" && row.benchmark_family_id === "livecodebench"));
});

test("query decoding canonicalizes unordered sets and rejects transport metadata and null filters", () => {
  const input = {
    ...golden.query.input,
    provider_ids: ["provider-b", "provider-a"],
    regions: ["us-west", "eu-west"],
  };
  const parsed = parseDecisionQueryV1(input);
  assert.deepEqual(parsed.provider_ids, ["provider-a", "provider-b"]);
  assert.deepEqual(parsed.regions, ["eu-west", "us-west"]);
  assert.throws(() => parseDecisionQueryV1({ ...input, request_id: "transport" }), /unknown fields/);
  assert.throws(() => parseDecisionQueryV1({ ...input, provider_ids: null }), /must not be null/);
  assert.throws(
    () => parseDecisionQueryV1({ ...input, provider_ids: ["provider-a", "provider-a"] }),
    /unique/,
  );
  assert.throws(
    () => parseDecisionQueryV1({
      ...input,
      objective: "capability_top_set",
      input_tokens_per_request: undefined,
      output_tokens_per_request: undefined,
      requests_per_month: undefined,
    }),
    /safe integer|monthly_budget_microusd/,
  );
});

test("typed provenance and observations fail closed", () => {
  const provenance = {
    object: "run_provenance",
    schema_version: "1",
    run_id: "run-public-01",
    benchmark_family_id: "livecodebench",
    feed_id: "livecodebench-discovery",
    source_artifact_id: `artifact_${"a".repeat(64)}`,
    parser_id: "json-parser",
    parser_version: "1",
    started_at: "2026-07-09T00:00:00Z",
    completed_at: "2026-07-09T00:01:00Z",
    harness_version: null,
    environment_digest: null,
    scorer_version: null,
    trial_policy: null,
    adapter_metadata: null,
  };
  assert.equal(parseRunProvenanceV1(provenance).feed_id, "livecodebench-discovery");
  assert.throws(() => parseRunProvenanceV1({ ...provenance, source: "mutable-latest" }), /unknown fields/);

  const observation = {
    object: "observation",
    schema_version: "1",
    observation_id: "obs_public_01",
    evaluated_configuration_id: `config_${"b".repeat(64)}`,
    metric: { kind: "proportion", value: "0.75", numerator: 3, denominator: 4 },
    uncertainty: { kind: "unknown" },
    provenance,
  };
  assert.equal(parseObservationV1(observation).metric.kind, "proportion");
  assert.throws(
    () => parseObservationV1({ ...observation, metric: { kind: "proportion", value: 0.75, numerator: 3, denominator: 4 } }),
    /value/,
  );
  assert.equal(
    parseObservationV1({ ...observation, metric: { kind: "proportion", value: "0.333333", numerator: 1, denominator: 3 } }).metric.kind,
    "proportion",
  );
  assert.throws(
    () => parseObservationV1({ ...observation, metric: { kind: "proportion", value: "0.5", numerator: 1, denominator: 3 } }),
    /six fractional digits|rounded half-even/,
  );
  assert.throws(
    () => parseObservationV1({ ...observation, metric: { kind: "proportion", value: "0", numerator: 1, denominator: 2 } }),
    /six fractional digits/,
  );
});

test("offer-link eligibility is exact, approved, and evaluated at the caller's as-of time", () => {
  const link = {
    object: "evaluation_to_offer_link",
    schema_version: "1",
    evaluation_to_offer_link_id: "link_public-demo",
    evaluated_configuration_id: `config_${"b".repeat(64)}`,
    serving_offer_id: "offer_public-demo",
    compatibility: "exact" as const,
    evidence_source_artifact_id: `artifact_${"a".repeat(64)}`,
    observed_at: "2026-07-09T00:00:00Z",
    expires_at: "2026-07-10T00:00:00Z",
    review_state: "approved" as const,
  };
  assert.equal(isEvaluationToOfferLinkEligible(link, "2026-07-09T12:00:00Z"), true);
  assert.equal(isEvaluationToOfferLinkEligible({ ...link, review_state: "pending" }, "2026-07-09T12:00:00Z"), false);
  assert.equal(isEvaluationToOfferLinkEligible(link, "2026-07-10T00:00:00Z"), false);
  assert.equal("eligible" in link, false);

  const fact = {
    observed_at: "2026-07-09T00:00:00Z",
    expires_at: "2026-07-10T00:00:00Z",
    source_artifact_id: `artifact_${"a".repeat(64)}`,
  };
  const offer = parseServingOfferV1({
    object: "serving_offer",
    schema_version: "1",
    serving_offer_id: "offer_public-demo",
    provider_id: "provider-public",
    sku: "public-demo",
    region: "us-west",
    context: { context_window_tokens: 128000, ...fact },
    availability: { status: "available", ...fact },
    pricing: {
      input_microusd_per_million_tokens: 1000000,
      output_microusd_per_million_tokens: 4800000,
      ...fact,
    },
  });
  assert.equal(isServingOfferDecisionEligible(offer, link, "2026-07-09T12:00:00Z"), true);
  assert.equal(
    isServingOfferDecisionEligible({ ...offer, availability: { ...offer.availability, status: "unavailable" } }, link, "2026-07-09T12:00:00Z"),
    false,
  );
  assert.equal(isServingOfferDecisionEligible(offer, link, "2026-07-10T00:00:00Z"), false);
});

test("receipt parsing verifies the full-body hash", async () => {
  const wire = { ...golden.receipt.body, receipt_id: golden.receipt.receipt_id };
  assert.equal((await parseDecisionReceiptV1(wire)).receipt_id, golden.receipt.receipt_id);
  await assert.rejects(
    () => parseDecisionReceiptV1({ ...wire, methodology_version: "2026-07-09.2.changed" }),
    /receipt_id/,
  );

  const unsortedBody = structuredClone(golden.receipt.body);
  (unsortedBody.evidence as unknown[]).reverse();
  (unsortedBody.sensitivity as unknown[]).reverse();
  assert.equal(await receiptId(unsortedBody), golden.receipt.receipt_id);

  await assert.rejects(
    () => parseDecisionReceiptV1({ ...wire, reasons: [] }),
    /reasons/,
  );
  const badSensitivity = structuredClone(wire);
  (badSensitivity.sensitivity as Array<Record<string, unknown>>)[0].selected_configuration_ids = [`config_${"b".repeat(64)}`];
  await assert.rejects(() => parseDecisionReceiptV1(badSensitivity), /sensitivity|leave_one_family_out/);

  await assert.rejects(
    () => parseDecisionReceiptV1({ ...wire, decided_at: "2026-07-10T00:00:00Z" }),
    /decided_at|current/,
  );
  const wrongCost = structuredClone(wire);
  (wrongCost.selections as Array<Record<string, unknown>>)[0].estimated_monthly_cost_microusd = 43000000;
  await assert.rejects(() => parseDecisionReceiptV1(wrongCost), /computed monthly cost/);
  const missingLinkEvidence = structuredClone(wire);
  missingLinkEvidence.evidence = (missingLinkEvidence.evidence as Array<Record<string, unknown>>)
    .filter((row) => row.kind !== "evaluation_to_offer_link");
  await assert.rejects(() => parseDecisionReceiptV1(missingLinkEvidence), /offer-link evidence|cited evidence_id/);

  const unequalCosts = structuredClone(wire);
  (unequalCosts.selections as Array<Record<string, unknown>>).push({
    evaluated_configuration_id: `config_${"c".repeat(64)}`,
    serving_offer_id: "offer_public-demo-two",
    capability_rank: 2,
    estimated_monthly_cost_microusd: 45000000,
  });
  await assert.rejects(() => parseDecisionReceiptV1(unequalCosts), /equal minimum cost/);

  const duplicateConfiguration = structuredClone(wire);
  (duplicateConfiguration.selections as Array<Record<string, unknown>>).push({
    ...(duplicateConfiguration.selections as Array<Record<string, unknown>>)[0],
    serving_offer_id: "offer_public-demo-two",
  });
  await assert.rejects(() => parseDecisionReceiptV1(duplicateConfiguration), /selections must be unique/);
});

test("snapshot-set IDs hash one normalized float-free descriptor", async () => {
  const descriptor = {
    object: "snapshot_set_descriptor" as const,
    schema_version: "1" as const,
    cell_id: "code-generation",
    manifest_version: "2026-07-09.2",
    methodology_version: "2026-07-09.2.public-decision-v1",
    ranking_group_snapshots: [
      { ranking_group_id: "rg-b", publication_snapshot_id: `snapshot_${"b".repeat(64)}` },
      { ranking_group_id: "rg-a", publication_snapshot_id: `snapshot_${"a".repeat(64)}` },
    ],
  };
  assert.equal(await snapshotSetId(descriptor), await snapshotSetId({
    ...descriptor,
    ranking_group_snapshots: [...descriptor.ranking_group_snapshots].reverse(),
  }));
  assert.throws(() => parseSnapshotSetDescriptorV1(descriptor), /sorted on the wire/);
  assert.equal(
    parseSnapshotSetDescriptorV1({
      ...descriptor,
      ranking_group_snapshots: [...descriptor.ranking_group_snapshots].reverse(),
    }).ranking_group_snapshots[0].ranking_group_id,
    "rg-a",
  );
  assert.throws(
    () => parseSnapshotSetDescriptorV1({
      ...descriptor,
      ranking_group_snapshots: [{
        ...descriptor.ranking_group_snapshots[1],
        generated_at: "2026-07-09T00:00:00Z",
      }],
    }),
    /unknown fields/,
  );

  const orderedDescriptor = parseSnapshotSetDescriptorV1({
    ...descriptor,
    ranking_group_snapshots: [...descriptor.ranking_group_snapshots].reverse(),
  });
  const leaderboard = {
    cell_id: orderedDescriptor.cell_id,
    manifest_version: orderedDescriptor.manifest_version,
    methodology_version: orderedDescriptor.methodology_version,
    snapshot_set_id: await snapshotSetId(orderedDescriptor),
    snapshot_set_descriptor: orderedDescriptor,
    ranking_groups: orderedDescriptor.ranking_group_snapshots,
  };
  assert.equal((await verifyLeaderboardSnapshotSet(leaderboard)).cell_id, "code-generation");
  await assert.rejects(
    () => verifyLeaderboardSnapshotSet({
      ...leaderboard,
      ranking_groups: [{
        ranking_group_id: "rg-a",
        publication_snapshot_id: `snapshot_${"c".repeat(64)}`,
      }],
    }),
    /exact ranking-group snapshot pairs/,
  );
  await assert.rejects(
    () => verifyLeaderboardSnapshotSet({
      ...leaderboard,
      ranking_groups: [
        { ranking_group_id: "rg-a", publication_snapshot_id: `snapshot_${"b".repeat(64)}` },
        { ranking_group_id: "rg-b", publication_snapshot_id: `snapshot_${"a".repeat(64)}` },
      ],
    }),
    /exact ranking-group snapshot pairs/,
  );
});

test("read semantic verifiers reject the same leaderboard mutations as Python", async () => {
  const leaderboard = await activeLeaderboard();
  assert.equal(
    (await verifyLeaderboardSemantics(leaderboard)).cell_id,
    "code-generation",
  );

  const duplicateConfiguration = structuredClone(leaderboard);
  const duplicateEntry = structuredClone(duplicateConfiguration.ranking_groups[0].entries[0]);
  duplicateEntry.ranking.rank = 2;
  duplicateConfiguration.ranking_groups[0].entries.push(duplicateEntry);
  duplicateConfiguration.ranking_groups[0].eligibility_summary.rank_eligible_configuration_count = 2;
  await assert.rejects(
    () => verifyLeaderboardSemantics(duplicateConfiguration),
    /evaluated_configuration_id values must be unique/,
  );

  const noncontiguousRanks = structuredClone(leaderboard);
  noncontiguousRanks.ranking_groups[0].entries[0].ranking.rank = 2;
  await assert.rejects(
    () => verifyLeaderboardSemantics(noncontiguousRanks),
    /contiguous from 1/,
  );

  const invertedInterval = structuredClone(leaderboard);
  invertedInterval.ranking_groups[0].entries[0].ranking.uncertainty = {
    kind: "interval",
    level: 0.95,
    lower: 0.9,
    upper: 0.8,
  };
  await assert.rejects(
    () => verifyLeaderboardSemantics(invertedInterval),
    /lower must be <= upper/,
  );

  const falseGap = previewLeaderboard(leaderboard);
  falseGap.ranking_groups[0].eligibility_summary.gap_codes.push(
    "insufficient_independent_families",
  );
  await assert.rejects(
    () => verifyLeaderboardSemantics(falseGap),
    /insufficient_independent_families/,
  );

  const previewTopSet = previewLeaderboard(leaderboard);
  previewTopSet.ranking_groups[0].entries[0].ranking.in_top_set = true;
  await assert.rejects(
    () => verifyLeaderboardSemantics(previewTopSet),
    /non-active reads cannot claim top-set membership/,
  );

  const duplicateGroup = structuredClone(leaderboard);
  duplicateGroup.ranking_groups.push(structuredClone(duplicateGroup.ranking_groups[0]));
  await assert.rejects(
    () => verifyLeaderboardSemantics(duplicateGroup),
    /one-to-one|unique ranking_group_id|ranking_group_id values must be unique/,
  );
});

test("entity and compare semantic verifiers bind ownership and reject parity mutations", async () => {
  const leaderboard = await activeLeaderboard();
  const group = leaderboard.ranking_groups[0];
  const passport = {
    object: "configuration_passport" as const,
    schema_version: "1" as const,
    entity_kind: "model_configuration" as const,
    canonical_name: "Example",
    revision: "1",
    interaction_policy: "direct_prompt" as const,
    configuration_passport_class: "model-configuration-v1" as const,
    harness: null,
    scaffold: null,
    tools: [],
    quantization: null,
    system_prompt_policy: null,
    environment: null,
  };
  const evaluated_configuration_id = await evaluatedConfigurationId(passport);
  const common = {
    cell_id: leaderboard.cell_id,
    manifest_version: leaderboard.manifest_version,
    methodology_version: leaderboard.methodology_version,
    snapshot_set_id: leaderboard.snapshot_set_id,
    snapshot_set_descriptor: leaderboard.snapshot_set_descriptor,
    ranking_group_id: group.ranking_group_id,
    publication_snapshot_id: group.publication_snapshot_id,
    state: "active",
    eligibility_summary: group.eligibility_summary,
  };
  const ranking = structuredClone(group.entries[0].ranking);
  const entity = {
    ...common,
    entity: {
      evaluated_configuration: {
        object: "evaluated_configuration",
        schema_version: "1",
        evaluated_configuration_id,
        passport,
      },
      ranking,
    },
  };
  const compare = {
    ...common,
    entities: [
      { evaluated_configuration_id, ranking: structuredClone(ranking) },
      {
        evaluated_configuration_id: `config_${"d".repeat(64)}`,
        ranking: { ...structuredClone(ranking), rank: 2 },
      },
    ],
  };
  await verifyEntityDetailSemantics(entity);
  await verifyCompareResultSemantics(compare);

  for (const [document, verifier] of [
    [entity, verifyEntityDetailSemantics],
    [compare, verifyCompareResultSemantics],
  ] as const) {
    await assert.rejects(
      () => verifier({ ...document, ranking_group_id: "rg-other" }),
      /ranking-group snapshot pair/,
    );
  }

  const duplicateCompare = structuredClone(compare);
  duplicateCompare.entities[1].evaluated_configuration_id = evaluated_configuration_id;
  await assert.rejects(
    () => verifyCompareResultSemantics(duplicateCompare),
    /evaluated_configuration_id values must be unique/,
  );

  const duplicateRank = structuredClone(compare);
  duplicateRank.entities[1].ranking.rank = 1;
  await assert.rejects(
    () => verifyCompareResultSemantics(duplicateRank),
    /compare ranks must be unique/,
  );

  const previewEntity = structuredClone(entity);
  previewEntity.state = "preview";
  previewEntity.eligibility_summary = previewEligibility();
  await assert.rejects(
    () => verifyEntityDetailSemantics(previewEntity),
    /non-active reads cannot claim top-set membership/,
  );
});

async function activeLeaderboard() {
  const ranking_group_id = "rg-code-generation-model";
  const publication_snapshot_id = `snapshot_${"a".repeat(64)}`;
  const snapshot_set_descriptor = parseSnapshotSetDescriptorV1({
    object: "snapshot_set_descriptor",
    schema_version: "1",
    cell_id: "code-generation",
    manifest_version: "2026-07-09.2",
    methodology_version: "2026-07-09.2.truth-kernel-v1",
    ranking_group_snapshots: [{ ranking_group_id, publication_snapshot_id }],
  });
  return {
    cell_id: snapshot_set_descriptor.cell_id,
    manifest_version: snapshot_set_descriptor.manifest_version,
    methodology_version: snapshot_set_descriptor.methodology_version,
    snapshot_set_id: await snapshotSetId(snapshot_set_descriptor),
    snapshot_set_descriptor,
    ranking_groups: [{
      ranking_group_id,
      entity_kind: "model_configuration",
      state: "active",
      publication_snapshot_id,
      eligibility_summary: {
        published_claim: "top_set",
        rank_eligible_configuration_count: 1,
        current_independent_family_count: 3,
        required_independent_family_count: 3,
        current_overlap_count: 2,
        required_overlap_count: 2,
        calibration_status: "validated",
        gap_codes: [] as string[],
      },
      entries: [{
        evaluated_configuration_id: `config_${"c".repeat(64)}`,
        ranking: {
          rank: 1,
          display_name: "Example",
          capability_score: 0.8,
          uncertainty: {
            kind: "interval",
            level: 0.95,
            lower: 0.75,
            upper: 0.85,
          },
          in_top_set: true,
        },
      }],
    }],
  };
}

function previewLeaderboard<T extends Awaited<ReturnType<typeof activeLeaderboard>>>(
  leaderboard: T,
): T {
  const preview = structuredClone(leaderboard);
  preview.ranking_groups[0].state = "preview";
  preview.ranking_groups[0].eligibility_summary = previewEligibility();
  preview.ranking_groups[0].entries[0].ranking.in_top_set = false;
  return preview;
}

function previewEligibility() {
  return {
    published_claim: "explorer",
    rank_eligible_configuration_count: 1,
    current_independent_family_count: 3,
    required_independent_family_count: 3,
    current_overlap_count: 2,
    required_overlap_count: 2,
    calibration_status: "unvalidated",
    gap_codes: ["calibration_unvalidated"],
  };
}

test("Draft 2020 schemas enforce the portable semantic shapes they can express", () => {
  const names = [
    "source-artifact", "run-provenance", "observation", "configuration-passport",
    "evaluated-configuration", "serving-offer", "evaluation-to-offer-link", "decision-query", "decision-receipt",
  ];
  const schemas = names.map((name) => JSON.parse(
    readFileSync(new URL(`../../../schemas/${name}.schema.json`, import.meta.url), "utf8"),
  ));
  const ajv = new Ajv2020({
    allErrors: true,
    strict: false,
    formats: { uri: true, "uri-reference": true },
  });
  schemas.forEach((schema) => ajv.addSchema(schema));

  const queryValidator = ajv.getSchema("https://evalrank.ai/schemas/decision-query.schema.json")!;
  const receiptValidator = ajv.getSchema("https://evalrank.ai/schemas/decision-receipt.schema.json")!;
  const observationValidator = ajv.getSchema("https://evalrank.ai/schemas/observation.schema.json")!;
  assert.equal(queryValidator(golden.query.input), true, ajv.errorsText(queryValidator.errors));
  assert.equal(
    receiptValidator({ ...golden.receipt.body, receipt_id: golden.receipt.receipt_id }),
    true,
    ajv.errorsText(receiptValidator.errors),
  );

  const partialUsage = structuredClone(golden.query.input);
  delete partialUsage.output_tokens_per_request;
  assert.equal(queryValidator(partialUsage), false);

  const emptyReasons = { ...golden.receipt.body, receipt_id: golden.receipt.receipt_id, reasons: [] };
  assert.equal(receiptValidator(emptyReasons), false);
  const missingLeaveOneOut = structuredClone({ ...golden.receipt.body, receipt_id: golden.receipt.receipt_id });
  missingLeaveOneOut.sensitivity = (missingLeaveOneOut.sensitivity as Array<Record<string, unknown>>)
    .filter((row) => row.scenario !== "leave_one_family_out");
  assert.equal(receiptValidator(missingLeaveOneOut), false);

  const honestCostAbstention = structuredClone({
    ...golden.receipt.body,
    receipt_id: golden.receipt.receipt_id,
  });
  honestCostAbstention.outcome = "abstain";
  honestCostAbstention.selections = [];
  honestCostAbstention.exclusions = [];
  honestCostAbstention.reasons = [];
  honestCostAbstention.sensitivity = [];
  honestCostAbstention.evidence = [];
  honestCostAbstention.abstention_reason = "no_eligible_serving_offer";
  assert.equal(
    receiptValidator(honestCostAbstention),
    true,
    ajv.errorsText(receiptValidator.errors),
  );

  const invalidComparisonThreshold = structuredClone({
    ...golden.receipt.body,
    receipt_id: golden.receipt.receipt_id,
  });
  const contextReason = (invalidComparisonThreshold.reasons as Array<Record<string, unknown>>)
    .find((row) => row.code === "context_requirement_met")!;
  contextReason.threshold = null;
  assert.equal(receiptValidator(invalidComparisonThreshold), false);

  const invalidStatus = structuredClone({
    ...honestCostAbstention,
    reasons: [{
      reason_type: "avoid_when",
      code: "insufficient_evidence",
      subject_id: `config_${"a".repeat(64)}`,
      predicate: "unavailable",
      axis: "capability",
      observed_value: "invented-status",
      unit: "status",
      threshold: null,
      evidence_ids: ["evidence-observation"],
      freshness: honestCostAbstention.freshness,
      caveat_codes: [],
    }],
  });
  assert.equal(receiptValidator(invalidStatus), false);

  const provenance = {
    object: "run_provenance",
    schema_version: "1",
    run_id: "run-public-01",
    benchmark_family_id: "livecodebench",
    feed_id: "livecodebench-discovery",
    source_artifact_id: `artifact_${"a".repeat(64)}`,
    parser_id: "json-parser",
    parser_version: "1",
    started_at: "2026-07-09T00:00:00Z",
    completed_at: "2026-07-09T00:01:00Z",
    harness_version: null,
    environment_digest: null,
    scorer_version: null,
    trial_policy: null,
    adapter_metadata: null,
  };
  const observation = {
    object: "observation",
    schema_version: "1",
    observation_id: "obs_public_01",
    evaluated_configuration_id: `config_${"b".repeat(64)}`,
    metric: { kind: "proportion", value: "0.75", numerator: 3, denominator: 4 },
    uncertainty: { kind: "unknown" },
    provenance,
  };
  assert.equal(observationValidator(observation), true, ajv.errorsText(observationValidator.errors));
  assert.equal(observationValidator({ ...observation, metric: { ...observation.metric, value: "1.1" } }), false);
  assert.equal(observationValidator({ ...observation, metric: { ...observation.metric, denominator: 0 } }), false);
});
