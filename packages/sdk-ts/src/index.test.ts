import assert from "node:assert/strict";
import { test } from "node:test";
import http from "node:http";
import type { AddressInfo } from "node:net";
import {
  EvalRankApiError,
  EvalRankClient,
  type EvaluationRequest,
  type ProblemDetails,
  type Recommendation,
  type ScoringStageCatalog,
  type UseCaseCatalog,
} from "./index.ts";

test("EvalRankClient posts a public recommendation request", async () => {
  const server = await startServer(200, recommendationPayload());

  try {
    const recommendation = await new EvalRankClient(server.baseUrl).recommend(requestPayload());

    assert.equal(recommendation.object, "recommendation");
    assert.equal(server.method, "POST");
    assert.equal(server.path, "/v1/recommendations");
    assert.equal(server.headers["content-type"], "application/json");
    assert.equal(server.headers.accept, "application/json");
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

test("EvalRankClient fetches public use-case catalog metadata", async () => {
  const server = await startServer(200, useCaseCatalogPayload());

  try {
    const catalog = await new EvalRankClient(server.baseUrl).useCases();

    assert.equal(catalog.object, "use_case_catalog");
    assert.equal(server.method, "GET");
    assert.equal(server.path, "/v1/use-cases");
    assert.equal(server.headers.accept, "application/json");
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
    assert.equal(server.headers.accept, "application/json");
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
    methodology_version: "2026-06-25.1.public-fixture-v1",
    generated_at: "2026-06-25T00:00:00Z",
    use_cases: [
      {
        object: "use_case",
        id: "web-browsing",
        name: "Web browsing",
        definition: "Find and inspect public web information.",
        entity_kinds: ["agent", "tool"],
        rank_policy: "ranked",
        is_overlay: false,
      },
    ],
  };
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
    the_call: null,
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
