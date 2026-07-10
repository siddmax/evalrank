import assert from "node:assert/strict";
import { test } from "node:test";
import http from "node:http";
import { readFileSync } from "node:fs";
import type { AddressInfo } from "node:net";
import Ajv2020 from "ajv/dist/2020.js";
import {
  EvalRankApiError,
  EvalRankClient,
  parseProblemDetails,
  type EvaluationRequest,
  type ProblemDetails,
  type Recommendation,
  type ScoringStageCatalog,
  type UseCaseCatalog,
} from "./index.ts";

test("the public catalog manifest owns the exact 26-cell taxonomy", () => {
  const manifest = catalogManifest();
  const expected = [
    "code-generation",
    "autonomous-swe-agent",
    "function-calling",
    "mcp-tool-orchestration",
    "web-browsing",
    "computer-use",
    "deep-research",
    "customer-support",
    "enterprise-crm-workflow",
    "math-reasoning",
    "general-knowledge-qa",
    "rag-retrieval",
    "long-term-memory",
    "finance",
    "legal",
    "medical",
    "multilingual",
    "vision-multimodal",
    "web-frontend-code-generation",
    "devops-sre-terminal",
    "mobile-codegen",
    "reasoning",
    "factuality",
    "professional-deliverable-creation",
    "machine-learning-engineering",
    "computational-research-reproduction",
  ];

  assert.deepEqual(manifest.cells.map((cell) => cell.cell_id), expected);
  assert.ok(manifest.cells.every((cell) => cell.state === "preview"));
  assert.deepEqual(manifestUseCases(), manifest.cells.map((cell) => ({
    object: "use_case",
    id: cell.cell_id,
    name: cell.name,
    definition: cell.definition,
    entity_kinds: cell.entity_kinds,
    rank_policy: "ranked",
    is_overlay: false,
  })));
});

test("Ajv 2020 validates the canonical manifest and closed nested states", () => {
  const manifest = catalogManifest();
  const { ajv, validate, acceptsManifest } = manifestSchemaValidator();

  assert.equal(acceptsManifest(manifest), true, ajv.errorsText(validate.errors));

  const invalidCadence = structuredClone(manifest);
  invalidCadence.feeds[0].cadence.expected_seconds = 86_400;
  assert.equal(acceptsManifest(invalidCadence), false);

  const validatedCadence = structuredClone(manifest);
  validatedCadence.feeds[0].cadence = {
    status: "validated",
    mode: "periodic",
    expected_seconds: 86_400,
    stale_after_seconds: 172_800,
    stop_recommending_after_seconds: 604_800,
    as_of: null,
    upstream_version: null,
  };
  assert.equal(acceptsManifest(validatedCadence), true, ajv.errorsText(validate.errors));

  const misorderedCadence = structuredClone(validatedCadence);
  misorderedCadence.feeds[0].cadence.stale_after_seconds = 43_200;
  assert.equal(validate(misorderedCadence), true, ajv.errorsText(validate.errors));
  assert.equal(cadencesAreOrdered(misorderedCadence), false);
  assert.equal(acceptsManifest(misorderedCadence), false);

  const frozenCadence = structuredClone(manifest);
  frozenCadence.feeds[0].cadence = {
    status: "validated",
    mode: "frozen",
    expected_seconds: null,
    stale_after_seconds: null,
    stop_recommending_after_seconds: null,
    as_of: "2026-07-09T00:00:00Z",
    upstream_version: "v1",
  };
  assert.equal(acceptsManifest(frozenCadence), true, ajv.errorsText(validate.errors));

  const frozenCadenceWithFakeRecency = structuredClone(frozenCadence);
  frozenCadenceWithFakeRecency.feeds[0].cadence.stale_after_seconds = 86_400;
  assert.equal(acceptsManifest(frozenCadenceWithFakeRecency), false);

  const frozenCadenceWithoutVersion = structuredClone(frozenCadence);
  frozenCadenceWithoutVersion.feeds[0].cadence.upstream_version = null;
  assert.equal(acceptsManifest(frozenCadenceWithoutVersion), false);

  const invalidLineage = structuredClone(manifest);
  invalidLineage.feeds[0].lineage.validation_status = "validated";
  assert.equal(acceptsManifest(invalidLineage), false);

  const invalidCorrelation = structuredClone(manifest);
  const unknownFamily = invalidCorrelation.benchmark_families.find(
    (family) => family.correlation_status === "unknown",
  );
  assert.ok(unknownFamily);
  unknownFamily.correlated_family_group = "invented-group";
  assert.equal(acceptsManifest(invalidCorrelation), false);
});

test("Ajv 2020 rejects mixed identities and impossible ranking-group states", () => {
  const manifest = catalogManifest();
  const { ajv, validate, acceptsManifest } = manifestSchemaValidator();

  const invalidIdentity = structuredClone(manifest);
  const unresolved = invalidIdentity.ranking_groups.find((group) => group.entity_kind === "unresolved");
  assert.ok(unresolved);
  unresolved.claim_ceiling = "single_winner";
  assert.equal(acceptsManifest(invalidIdentity), false);

  for (const dimension of [
    "entity_kind",
    "interaction_policy",
    "configuration_passport_class",
  ] as const) {
    const mixedResolvedIdentity = structuredClone(manifest);
    const resolvedGroup = mixedResolvedIdentity.ranking_groups.find(
      (group) => group.entity_kind !== "unresolved",
    );
    assert.ok(resolvedGroup);
    resolvedGroup[dimension] = dimension === "configuration_passport_class"
      ? "unresolved-v1"
      : "unresolved";
    assert.equal(
      acceptsManifest(mixedResolvedIdentity),
      false,
      `a resolved identity cannot have unresolved ${dimension}`,
    );

    const mixedUnresolvedIdentity = structuredClone(manifest);
    const unresolvedGroup = mixedUnresolvedIdentity.ranking_groups.find(
      (group) => group.entity_kind === "unresolved",
    );
    assert.ok(unresolvedGroup);
    unresolvedGroup[dimension] = dimension === "configuration_passport_class"
      ? "model-configuration-v1"
      : dimension === "interaction_policy"
        ? "direct_prompt"
        : "model_configuration";
    assert.equal(
      acceptsManifest(mixedUnresolvedIdentity),
      false,
      `an unresolved identity cannot have resolved ${dimension}`,
    );

    const mixedResolvedFeedIdentity = structuredClone(manifest);
    const resolvedFeed = mixedResolvedFeedIdentity.feeds.find(
      (feed) => feed.entity_kind !== "unresolved",
    );
    assert.ok(resolvedFeed);
    resolvedFeed[dimension] = dimension === "configuration_passport_class"
      ? "unresolved-v1"
      : "unresolved";
    assert.equal(
      acceptsManifest(mixedResolvedFeedIdentity),
      false,
      `a resolved feed identity cannot have unresolved ${dimension}`,
    );

    const mixedUnresolvedFeedIdentity = structuredClone(manifest);
    const unresolvedFeed = mixedUnresolvedFeedIdentity.feeds.find(
      (feed) => feed.entity_kind === "unresolved",
    );
    assert.ok(unresolvedFeed);
    unresolvedFeed[dimension] = dimension === "configuration_passport_class"
      ? "model-configuration-v1"
      : dimension === "interaction_policy"
        ? "direct_prompt"
        : "model_configuration";
    assert.equal(
      acceptsManifest(mixedUnresolvedFeedIdentity),
      false,
      `an unresolved feed identity cannot have resolved ${dimension}`,
    );
  }

  const unknownUnresolvedPassport = structuredClone(manifest);
  unknownUnresolvedPassport.ranking_groups.find(
    (group) => group.entity_kind !== "unresolved",
  )!.configuration_passport_class = "unresolved-v2";
  assert.equal(acceptsManifest(unknownUnresolvedPassport), false);

  const incoherentResolvedIdentity = structuredClone(manifest);
  const modelGroup = incoherentResolvedIdentity.ranking_groups.find(
    (group) => group.entity_kind === "model_configuration",
  );
  assert.ok(modelGroup);
  modelGroup.interaction_policy = "agentic";
  modelGroup.configuration_passport_class = "agent-system-v1";
  assert.equal(acceptsManifest(incoherentResolvedIdentity), false);

  const validResolvedExplorer = structuredClone(manifest);
  const explorerGroup = validResolvedExplorer.ranking_groups.find(
    (group) => group.entity_kind !== "unresolved",
  );
  assert.ok(explorerGroup);
  explorerGroup.claim_ceiling = "explorer";
  explorerGroup.eligibility.top_set = null;
  explorerGroup.eligibility.single_winner = null;
  explorerGroup.eligibility.superiority_threshold = null;
  explorerGroup.eligibility.practical_effect_floor = null;
  explorerGroup.eligibility.leave_one_family_out = null;
  assert.equal(acceptsManifest(validResolvedExplorer), true, ajv.errorsText(validate.errors));

  const activeExplorer = structuredClone(validResolvedExplorer);
  const invalidActiveExplorer = activeExplorer.ranking_groups.find(
    (group) => group.ranking_group_id === explorerGroup.ranking_group_id,
  );
  assert.ok(invalidActiveExplorer);
  invalidActiveExplorer.state = "active";
  invalidActiveExplorer.rank_eligible_count = 1;
  invalidActiveExplorer.eligibility.calibration_status = "validated";
  assert.equal(acceptsManifest(activeExplorer), false);

  const validActiveGroup = structuredClone(manifest);
  const activeGroup = validActiveGroup.ranking_groups.find(
    (group) => group.state === "preview" && group.entity_kind !== "unresolved",
  );
  assert.ok(activeGroup);
  activeGroup.state = "active";
  activeGroup.rank_eligible_count = 2;
  activeGroup.eligibility.calibration_status = "validated";
  assert.ok(activeGroup.eligibility.practical_effect_floor);
  activeGroup.eligibility.practical_effect_floor.status = "validated";
  assert.equal(acceptsManifest(validActiveGroup), true, ajv.errorsText(validate.errors));

  const activeGroupWithoutCalibration = structuredClone(validActiveGroup);
  activeGroupWithoutCalibration.ranking_groups.find(
    (group) => group.ranking_group_id === activeGroup.ranking_group_id,
  )!.eligibility.calibration_status = "unvalidated";
  assert.equal(acceptsManifest(activeGroupWithoutCalibration), false);

  const activeGroupWithoutCalibratedEffect = structuredClone(validActiveGroup);
  activeGroupWithoutCalibratedEffect.ranking_groups.find(
    (group) => group.ranking_group_id === activeGroup.ranking_group_id,
  )!.eligibility.practical_effect_floor = {
    mode: "native-metric-calibrated",
    status: "unvalidated",
  };
  assert.equal(acceptsManifest(activeGroupWithoutCalibratedEffect), false);

  for (const invalidCount of [0, 1, null] as const) {
    const activeGroupWithoutCount = structuredClone(validActiveGroup);
    activeGroupWithoutCount.ranking_groups.find(
      (group) => group.ranking_group_id === activeGroup.ranking_group_id,
    )!.rank_eligible_count = invalidCount;
    assert.equal(acceptsManifest(activeGroupWithoutCount), false);
  }

  const activeUnresolvedGroup = structuredClone(manifest);
  const unresolvedActive = activeUnresolvedGroup.ranking_groups.find(
    (group) => group.entity_kind === "unresolved",
  );
  assert.ok(unresolvedActive);
  unresolvedActive.state = "active";
  unresolvedActive.rank_eligible_count = 1;
  unresolvedActive.eligibility.calibration_status = "validated";
  assert.equal(acceptsManifest(activeUnresolvedGroup), false);

  const previewGroupWithCount = structuredClone(manifest);
  previewGroupWithCount.ranking_groups.find(
    (group) => group.state === "preview",
  )!.rank_eligible_count = 1;
  assert.equal(acceptsManifest(previewGroupWithCount), true, ajv.errorsText(validate.errors));

  const quarantinedGroupWithoutReason = structuredClone(manifest);
  quarantinedGroupWithoutReason.ranking_groups.find(
    (group) => group.state === "quarantined",
  )!.quarantine_reason = null;
  assert.equal(acceptsManifest(quarantinedGroupWithoutReason), false);

  const quarantinedGroupWithCount = structuredClone(manifest);
  quarantinedGroupWithCount.ranking_groups.find(
    (group) => group.state === "quarantined",
  )!.rank_eligible_count = 1;
  assert.equal(acceptsManifest(quarantinedGroupWithCount), false);

  const previewGroupWithReason = structuredClone(manifest);
  previewGroupWithReason.ranking_groups.find(
    (group) => group.state === "preview",
  )!.quarantine_reason = "This must remain null outside quarantine.";
  assert.equal(acceptsManifest(previewGroupWithReason), false);
});

test("Ajv 2020 enforces fail-closed family and feed admission states", () => {
  const manifest = catalogManifest();
  const { ajv, validate, acceptsManifest } = manifestSchemaValidator();

  const discoveredFamilyWithCount = structuredClone(manifest);
  discoveredFamilyWithCount.benchmark_families.find(
    (family) => family.state === "discovered",
  )!.rank_eligible_count = 1;
  assert.equal(acceptsManifest(discoveredFamilyWithCount), false);

  const quarantinedFamilyWithoutReason = structuredClone(manifest);
  quarantinedFamilyWithoutReason.benchmark_families.find(
    (family) => family.state === "quarantined",
  )!.quarantine_reason = null;
  assert.equal(acceptsManifest(quarantinedFamilyWithoutReason), false);

  const discoveredFamilyWithReason = structuredClone(manifest);
  discoveredFamilyWithReason.benchmark_families.find(
    (family) => family.state === "discovered",
  )!.quarantine_reason = "This must remain null outside quarantine.";
  assert.equal(acceptsManifest(discoveredFamilyWithReason), false);

  const validActiveFamily = structuredClone(manifest);
  const admittedFamily = validActiveFamily.benchmark_families.find(
    (family) => family.state === "discovered",
  );
  assert.ok(admittedFamily);
  admittedFamily.state = "active";
  admittedFamily.rank_eligible_count = 1;
  admittedFamily.correlation_status = "validated";
  admittedFamily.correlated_family_group = "independent-family-v1";
  assert.equal(acceptsManifest(validActiveFamily), true, ajv.errorsText(validate.errors));

  for (const [requirement, breakAdmission] of [
    ["rank count", (family: ManifestFamily) => { family.rank_eligible_count = null; }],
    ["positive rank count", (family: ManifestFamily) => { family.rank_eligible_count = 0; }],
    ["validated correlation", (family: ManifestFamily) => {
      family.correlation_status = "unknown";
      family.correlated_family_group = null;
    }],
    ["correlation group", (family: ManifestFamily) => {
      family.correlated_family_group = null;
    }],
  ] as const) {
    const invalidActiveFamily = structuredClone(validActiveFamily);
    const family = invalidActiveFamily.benchmark_families.find(
      (row) => row.benchmark_family_id === admittedFamily.benchmark_family_id,
    );
    assert.ok(family);
    breakAdmission(family);
    assert.equal(
      acceptsManifest(invalidActiveFamily),
      false,
      `active family admission requires ${requirement}`,
    );
  }

  const activeUnresolvedFamily = structuredClone(validActiveFamily);
  activeUnresolvedFamily.benchmark_families.find(
    (row) => row.benchmark_family_id === admittedFamily.benchmark_family_id,
  )!.entity_kinds = ["unresolved"];
  assert.equal(acceptsManifest(activeUnresolvedFamily), false);

  const discoveredFeedWithAdapter = structuredClone(manifest);
  discoveredFeedWithAdapter.feeds.find((feed) => feed.state === "discovered")!.adapter_id =
    "adapter-v1";
  assert.equal(acceptsManifest(discoveredFeedWithAdapter), false);

  const discoveredFeedWithCount = structuredClone(manifest);
  discoveredFeedWithCount.feeds.find((feed) => feed.state === "discovered")!.rank_eligible_count = 1;
  assert.equal(acceptsManifest(discoveredFeedWithCount), false);

  const shadowFeedWithoutAdapter = structuredClone(manifest);
  shadowFeedWithoutAdapter.feeds.find((feed) => feed.state === "discovered")!.state = "shadow";
  assert.equal(acceptsManifest(shadowFeedWithoutAdapter), false);

  const validShadowFeed = structuredClone(manifest);
  const shadowFeed = validShadowFeed.feeds.find((feed) => feed.state === "discovered");
  assert.ok(shadowFeed);
  shadowFeed.state = "shadow";
  shadowFeed.adapter_id = "adapter-v1";
  assert.equal(acceptsManifest(validShadowFeed), true, ajv.errorsText(validate.errors));

  const validActiveFeed = structuredClone(manifest);
  const admittedFeed = validActiveFeed.feeds.find((feed) => feed.state === "discovered");
  assert.ok(admittedFeed);
  admittedFeed.state = "active";
  admittedFeed.adapter_id = "adapter-v1";
  admittedFeed.rank_eligible_count = 1;
  admittedFeed.retention.store_artifact_bytes = true;
  admittedFeed.rights = {
    ...admittedFeed.rights,
    status: "approved",
    harness_code_license: "Apache-2.0",
    task_data_license: "approved-evaluation-terms",
    commercial_use: "allowed",
    result_redistribution: "allowed",
    environment_terms: "allowed",
    artifact_retention: "allowed",
    derived_score_publication: "allowed",
  };
  admittedFeed.cadence = {
    status: "validated",
    mode: "periodic",
    expected_seconds: 86_400,
    stale_after_seconds: 172_800,
    stop_recommending_after_seconds: 604_800,
    as_of: null,
    upstream_version: null,
  };
  admittedFeed.lineage = {
    ...admittedFeed.lineage,
    validation_status: "validated",
    task_lineage_id: "task-lineage-v1",
    environment_lineage_id: "environment-lineage-v1",
    grader_lineage_id: "grader-lineage-v1",
    correlation_status: "validated",
    correlated_family_group: "independent-family-v1",
  };
  assert.equal(acceptsManifest(validActiveFeed), true, ajv.errorsText(validate.errors));

  const activeUnresolvedFeed = structuredClone(validActiveFeed);
  const unresolvedFeed = activeUnresolvedFeed.feeds.find(
    (row) => row.feed_id === admittedFeed.feed_id,
  );
  assert.ok(unresolvedFeed);
  unresolvedFeed.entity_kind = "unresolved";
  unresolvedFeed.interaction_policy = "unresolved";
  unresolvedFeed.configuration_passport_class = "unresolved-v1";
  assert.equal(acceptsManifest(activeUnresolvedFeed), false);

  for (const [requirement, breakAdmission] of [
    ["adapter", (feed: ManifestFeed) => { feed.adapter_id = null; }],
    ["rank count", (feed: ManifestFeed) => { feed.rank_eligible_count = 0; }],
    ["rights", (feed: ManifestFeed) => { feed.rights.status = "unknown"; }],
    ["harness license review", (feed: ManifestFeed) => {
      feed.rights.harness_code_license = null;
    }],
    ["task-data license review", (feed: ManifestFeed) => {
      feed.rights.task_data_license = null;
    }],
    ["commercial-use rights", (feed: ManifestFeed) => {
      feed.rights.commercial_use = "unknown";
    }],
    ["result redistribution rights", (feed: ManifestFeed) => {
      feed.rights.result_redistribution = "blocked";
    }],
    ["known result redistribution rights", (feed: ManifestFeed) => {
      feed.rights.result_redistribution = "unknown";
    }],
    ["environment terms", (feed: ManifestFeed) => {
      feed.rights.environment_terms = "unknown";
    }],
    ["derived-score publication rights", (feed: ManifestFeed) => {
      feed.rights.derived_score_publication = "blocked";
    }],
    ["known derived-score publication rights", (feed: ManifestFeed) => {
      feed.rights.derived_score_publication = "unknown";
    }],
    ["retention rights when bytes are stored", (feed: ManifestFeed) => {
      feed.retention.store_artifact_bytes = true;
      feed.rights.artifact_retention = "blocked";
    }],
    ["known retention rights when bytes are stored", (feed: ManifestFeed) => {
      feed.retention.store_artifact_bytes = true;
      feed.rights.artifact_retention = "unknown";
    }],
    ["replayable retained artifacts", (feed: ManifestFeed) => {
      feed.retention.store_artifact_bytes = false;
    }],
    ["cadence", (feed: ManifestFeed) => {
      feed.cadence = {
        status: "unvalidated",
        mode: null,
        expected_seconds: null,
        stale_after_seconds: null,
        stop_recommending_after_seconds: null,
        as_of: null,
        upstream_version: null,
      };
    }],
    ["lineage", (feed: ManifestFeed) => {
      feed.lineage.validation_status = "unknown";
      feed.lineage.task_lineage_id = null;
      feed.lineage.environment_lineage_id = null;
      feed.lineage.grader_lineage_id = null;
    }],
    ["validated correlation", (feed: ManifestFeed) => {
      feed.lineage.correlation_status = "declared";
    }],
    ["correlation group", (feed: ManifestFeed) => {
      feed.lineage.correlated_family_group = null;
    }],
  ] as const) {
    const invalidActiveFeed = structuredClone(validActiveFeed);
    const feed = invalidActiveFeed.feeds.find((row) => row.feed_id === admittedFeed.feed_id);
    assert.ok(feed);
    breakAdmission(feed);
    assert.equal(
      acceptsManifest(invalidActiveFeed),
      false,
      `active admission requires ${requirement}`,
    );
  }

  const quarantinedFeedWithoutReason = structuredClone(manifest);
  quarantinedFeedWithoutReason.feeds.find(
    (feed) => feed.state === "quarantined",
  )!.quarantine_reason = null;
  assert.equal(acceptsManifest(quarantinedFeedWithoutReason), false);

  const quarantinedFeedWithCount = structuredClone(manifest);
  quarantinedFeedWithCount.feeds.find(
    (feed) => feed.state === "quarantined",
  )!.rank_eligible_count = 1;
  assert.equal(acceptsManifest(quarantinedFeedWithCount), false);

  const discoveredFeedWithReason = structuredClone(manifest);
  discoveredFeedWithReason.feeds.find(
    (feed) => feed.state === "discovered",
  )!.quarantine_reason = "This must remain null outside quarantine.";
  assert.equal(acceptsManifest(discoveredFeedWithReason), false);
});

test("EvalRankClient posts a public recommendation request", async () => {
  const server = await startServer(200, recommendationPayload());

  try {
    const recommendation = await new EvalRankClient(server.baseUrl).recommend(requestPayload());

    assert.equal(recommendation.object, "recommendation");
    assert.equal(server.method, "POST");
    assert.equal(server.path, "/v1/recommendations");
    assert.equal(server.headers["content-type"], "application/json");
    assert.equal(server.headers.accept, "application/json, application/problem+json");
    assert.deepEqual(server.requestJson, requestPayload());
  } finally {
    await server.close();
  }
});

test("EvalRankClient raises public Problem Details errors", async () => {
  const problem: ProblemDetails = {
    type: "https://evalrank.ai/problems/rate-limited",
    title: "Rate limited",
    status: 429,
    detail: "too many requests",
    code: "rate_limited",
    retriable: true,
    retry_after: 3,
  };
  const server = await startServer(429, problem, {
    "Content-Type": "application/problem+json",
    "Retry-After": "3",
  });

  try {
    await assert.rejects(
      () => new EvalRankClient(server.baseUrl).recommend(requestPayload()),
      (error: unknown) => {
        assert.ok(error instanceof EvalRankApiError);
        assert.equal(error.status, 429);
        assert.equal(error.retryAfter, 3);
        assert.deepEqual(error.problem, problem);
        return true;
      },
    );
  } finally {
    await server.close();
  }
});

test("EvalRankClient treats malformed Retry-After as absent", async () => {
  const problem: ProblemDetails = {
    type: "https://evalrank.ai/problems/rate-limited",
    title: "Rate limited",
    status: 429,
    detail: "too many requests",
    code: "rate_limited",
    retriable: true,
    retry_after: 3,
  };
  const server = await startServer(429, problem, {
    "Content-Type": "application/problem+json",
    "Retry-After": "3 seconds",
  });

  try {
    await assert.rejects(
      () => new EvalRankClient(server.baseUrl).recommend(requestPayload()),
      (error: unknown) => {
        assert.ok(error instanceof EvalRankApiError);
        assert.equal(error.status, 429);
        assert.equal(error.retryAfter, null);
        assert.deepEqual(error.problem, problem);
        return true;
      },
    );
  } finally {
    await server.close();
  }
});

test("Problem Details decoding preserves unknown RFC 9457 extensions", () => {
  const payload = {
    type: "https://evalrank.ai/problems/rate-limited",
    title: "Rate limited",
    status: 429,
    detail: "too many requests",
    code: "rate_limited",
    retriable: true,
    provider_window: { limit: 100, seconds: 60 },
  };

  assert.deepEqual(parseProblemDetails(payload), payload);
});

test("Problem Details decoding rejects malformed known members", () => {
  const valid = {
    type: "about:blank",
    title: "Validation failed",
    status: 422,
    detail: "request_id is required",
  };
  for (const payload of [
    { ...valid, status: "422" },
    { ...valid, type: "not a uri reference" },
    { ...valid, type: "http://" },
    { ...valid, instance: "bad uri reference" },
    { ...valid, code: null },
    { ...valid, retriable: null },
    { ...valid, retry_after: 1.5 },
    { ...valid, retry_after: 2 ** 53 },
    { ...valid, doc_url: "file:///private" },
    { ...valid, doc_url: "http://" },
    { type: valid.type, title: valid.title, status: valid.status },
    [valid],
  ]) {
    assert.throws(() => parseProblemDetails(payload), /Problem Details/);
  }
});

test("Problem Details matches shared URI regression vectors", () => {
  const vectors = JSON.parse(
    readFileSync(
      new URL("../../../examples/problem-details-uri-v1.golden.json", import.meta.url),
      "utf8",
    ),
  );
  const valid = {
    title: "Validation failed",
    status: 422,
    detail: "request_id is required",
  };

  for (const type of vectors.uri_references.valid) {
    assert.deepEqual(parseProblemDetails({ ...valid, type }), { ...valid, type });
  }
  for (const type of vectors.uri_references.invalid) {
    assert.throws(() => parseProblemDetails({ ...valid, type }), /Problem Details/);
  }
  for (const doc_url of vectors.http_urls.valid) {
    assert.deepEqual(
      parseProblemDetails({ ...valid, type: "about:blank", doc_url }),
      { ...valid, type: "about:blank", doc_url },
    );
  }
  for (const doc_url of vectors.http_urls.invalid) {
    assert.throws(
      () => parseProblemDetails({ ...valid, type: "about:blank", doc_url }),
      /Problem Details/,
    );
  }
});

test("EvalRankClient fetches public use-case catalog metadata", async () => {
  const server = await startServer(200, useCaseCatalogPayload());

  try {
    const catalog = await new EvalRankClient(server.baseUrl).useCases();

    assert.equal(catalog.object, "use_case_catalog");
    assert.deepEqual(catalog.use_cases, manifestUseCases());
    assert.equal(server.method, "GET");
    assert.equal(server.path, "/v1/use-cases");
    assert.equal(server.headers.accept, "application/json, application/problem+json");
    assert.equal(server.requestBody, "");
  } finally {
    await server.close();
  }
});

test("EvalRankClient fetches public scoring-stage catalog metadata", async () => {
  const server = await startServer(200, scoringStageCatalogPayload());

  try {
    const catalog = await new EvalRankClient(server.baseUrl).scoringStages();

    assert.equal(catalog.object, "scoring_stage_catalog");
    assert.equal(server.method, "GET");
    assert.equal(server.path, "/v1/scoring-stages");
    assert.equal(server.headers.accept, "application/json, application/problem+json");
    assert.equal(server.requestBody, "");
  } finally {
    await server.close();
  }
});

test("EvalRankClient raises public Problem Details errors for metadata routes", async () => {
  const problem: ProblemDetails = {
    type: "https://evalrank.ai/problems/upstream-timeout",
    title: "Upstream timeout",
    status: 503,
    detail: "catalog temporarily unavailable",
    code: "upstream_timeout",
    retriable: true,
    retry_after: 5,
  };
  const server = await startServer(503, problem, {
    "Content-Type": "application/problem+json",
    "Retry-After": "5",
  });

  try {
    await assert.rejects(
      () => new EvalRankClient(server.baseUrl).useCases(),
      (error: unknown) => {
        assert.ok(error instanceof EvalRankApiError);
        assert.equal(error.status, 503);
        assert.equal(error.retryAfter, 5);
        assert.deepEqual(error.problem, problem);
        return true;
      },
    );
  } finally {
    await server.close();
  }
});

test("EvalRankClient rejects non-http base URLs", () => {
  assert.throws(
    () => new EvalRankClient("file:///tmp/evalrank"),
    /baseUrl must be an http or https URL/,
  );
});

async function startServer(
  responseStatus: number,
  responseBody: Record<string, unknown>,
  responseHeaders: Record<string, string> = {},
) {
  let method: string | null = null;
  let requestJson: unknown = null;
  let requestBody = "";
  let path: string | null = null;
  let headers: http.IncomingHttpHeaders = {};

  const server = http.createServer(async (request, response) => {
    method = request.method ?? null;
    path = request.url ?? null;
    headers = request.headers;
    requestBody = await readBody(request);
    requestJson = requestBody === "" ? null : JSON.parse(requestBody);
    const encoded = JSON.stringify(responseBody);
    response.writeHead(responseStatus, {
      "Content-Type": "application/json",
      "Content-Length": Buffer.byteLength(encoded),
      ...responseHeaders,
    });
    response.end(encoded);
  });

  await new Promise<void>((resolve) => server.listen(0, "127.0.0.1", resolve));
  const address = server.address() as AddressInfo;

  return {
    baseUrl: `http://${address.address}:${address.port}`,
    get headers() {
      return headers;
    },
    get method() {
      return method;
    },
    get path() {
      return path;
    },
    get requestJson() {
      return requestJson;
    },
    get requestBody() {
      return requestBody;
    },
    close: () => new Promise<void>((resolve, reject) => {
      server.close((error) => (error ? reject(error) : resolve()));
    }),
  };
}

function useCaseCatalogPayload(): UseCaseCatalog {
  return {
    object: "use_case_catalog",
    methodology_version: "2026-07-09.3.catalog-manifest-v1",
    generated_at: "2026-07-09T00:00:00Z",
    use_cases: manifestUseCases(),
  };
}

type ManifestCell = {
  cell_id: string;
  name: string;
  definition: string;
  entity_kinds: Array<"model" | "tool" | "agent">;
  state: string;
};

type CatalogManifest = {
  cells: ManifestCell[];
  ranking_groups: Array<{
    ranking_group_id: string;
    entity_kind: string;
    interaction_policy: string;
    configuration_passport_class: string;
    state: string;
    rank_eligible_count: number | null;
    quarantine_reason: string | null;
    claim_ceiling: string;
    eligibility: {
      calibration_status: string;
      top_set: unknown;
      single_winner: unknown;
      superiority_threshold: number | null;
      practical_effect_floor: unknown;
      leave_one_family_out: unknown;
    };
  }>;
  benchmark_families: Array<{
    benchmark_family_id: string;
    entity_kinds: string[];
    state: string;
    rank_eligible_count: number | null;
    quarantine_reason: string | null;
    correlation_status: string;
    correlated_family_group: string | null;
  }>;
  feeds: ManifestFeed[];
};

type ManifestFamily = CatalogManifest["benchmark_families"][number];

type ManifestFeed = {
  feed_id: string;
  adapter_id: string | null;
  entity_kind: string;
  interaction_policy: string;
  configuration_passport_class: string;
  state: string;
  rank_eligible_count: number | null;
  quarantine_reason: string | null;
  rights: {
    status: string;
    harness_code_license: string | null;
    task_data_license: string | null;
    commercial_use: string;
    result_redistribution: string;
    trajectory_redistribution: string;
    environment_terms: string;
    artifact_retention: string;
    derived_score_publication: string;
  };
  retention: {
    store_artifact_bytes: boolean;
    maximum_days: number | null;
  };
  cadence: {
    status: string;
    mode: "frozen" | "periodic" | null;
    expected_seconds: number | null;
    stale_after_seconds: number | null;
    stop_recommending_after_seconds: number | null;
    as_of: string | null;
    upstream_version: string | null;
  };
  lineage: {
    validation_status: string;
    task_lineage_id: string | null;
    environment_lineage_id: string | null;
    grader_lineage_id: string | null;
    correlation_status: string;
    correlated_family_group: string | null;
  };
};

function catalogManifest(): CatalogManifest {
  return JSON.parse(
    readFileSync(new URL("../../../catalog/manifest.json", import.meta.url), "utf8"),
  ) as CatalogManifest;
}

function manifestSchemaValidator() {
  const schema = JSON.parse(
    readFileSync(new URL("../../../schemas/evalrank-manifest.schema.json", import.meta.url), "utf8"),
  );
  const ajv = new Ajv2020({ allErrors: true, allowUnionTypes: true, strict: true });
  const validate = ajv.compile(schema);
  const acceptsManifest = (candidate: CatalogManifest) =>
    Boolean(validate(candidate)) && cadencesAreOrdered(candidate);
  return { ajv, validate, acceptsManifest };
}

function manifestUseCases(): UseCaseCatalog["use_cases"] {
  return catalogManifest().cells.map((cell) => ({
    object: "use_case",
    id: cell.cell_id,
    name: cell.name,
    definition: cell.definition,
    entity_kinds: cell.entity_kinds,
    rank_policy: "ranked",
    is_overlay: false,
  })) as UseCaseCatalog["use_cases"];
}

function cadencesAreOrdered(manifest: CatalogManifest): boolean {
  return manifest.feeds.every(({ cadence }) => {
    if (cadence.status === "unvalidated") {
      return cadence.mode === null
        && cadence.expected_seconds === null
        && cadence.stale_after_seconds === null
        && cadence.stop_recommending_after_seconds === null
        && cadence.as_of === null
        && cadence.upstream_version === null;
    }
    if (cadence.mode === "frozen") {
      return cadence.expected_seconds === null
        && cadence.stale_after_seconds === null
        && cadence.stop_recommending_after_seconds === null
        && cadence.as_of !== null
        && cadence.upstream_version !== null;
    }
    return cadence.mode === "periodic"
      && cadence.expected_seconds !== null
      && cadence.stale_after_seconds !== null
      && cadence.stop_recommending_after_seconds !== null
      && cadence.as_of === null
      && cadence.upstream_version === null
      && cadence.expected_seconds > 0
      && cadence.expected_seconds <= cadence.stale_after_seconds
      && cadence.stale_after_seconds <= cadence.stop_recommending_after_seconds;
  });
}

function scoringStageCatalogPayload(): ScoringStageCatalog {
  return {
    object: "scoring_stage_catalog",
    methodology_version: "2026-06-25.1.public-fixture-v1",
    generated_at: "2026-06-25T00:00:00Z",
    stages: [
      {
        id: "candidate-retrieval",
        ordinal: 1,
        name: "Candidate retrieval",
        description: "Build a public candidate set.",
        input_contracts: ["EvaluationRequest"],
        output_contracts: ["CandidateSet"],
        public_boundary: "storage-free public contract",
      },
    ],
  };
}

function readBody(request: http.IncomingMessage): Promise<string> {
  return new Promise((resolve, reject) => {
    let body = "";
    request.setEncoding("utf8");
    request.on("data", (chunk) => {
      body += chunk;
    });
    request.on("end", () => resolve(body));
    request.on("error", reject);
  });
}

function requestPayload(): EvaluationRequest {
  return {
    object: "evaluation_request",
    request_id: "req_public_fixture_01",
    use_case: "web-browsing",
    entity_types: ["mcp_server"],
    requested_at: "2026-06-25T00:00:00Z",
    constraints: {},
  };
}

function recommendationPayload(): Recommendation {
  return {
    object: "recommendation",
    use_case: "web-browsing",
    shortlist_depth: 1,
    depth_rationale: "public fixture",
    degraded: false,
    served_from: "public-fixture",
    base_snapshot_lag_ms: 0,
    methodology_version: "2026-06-25.1.public-fixture-v1",
    generated_at: "2026-06-25T00:00:00Z",
    comparability: "single-scale",
    ranked: [],
    groups: null,
    the_call: {
      decision: "abstain",
      confidence: null,
      reason: "insufficient_evidence",
      abstention_reason: "insufficient_evidence",
    },
    abstention: {
      reason: "insufficient_evidence",
      detail: "fixture-only response",
    },
    exclusions: [],
    recommendation_id: "rec_public_fixture_01",
    recommend_id: "rec_public_fixture_01",
    search_run_id: "rec_public_fixture_01",
    request_id: "req_public_fixture_01",
  };
}
