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
} from "./index.ts";

test("EvalRankClient posts a public recommendation request", async () => {
  const server = await startServer(200, recommendationPayload());

  try {
    const recommendation = await new EvalRankClient(server.baseUrl).recommend(requestPayload());

    assert.equal(recommendation.object, "recommendation");
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
  let requestJson: unknown = null;
  let path: string | null = null;
  let headers: http.IncomingHttpHeaders = {};

  const server = http.createServer(async (request, response) => {
    path = request.url ?? null;
    headers = request.headers;
    requestJson = JSON.parse(await readBody(request));
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
    get path() {
      return path;
    },
    get requestJson() {
      return requestJson;
    },
    close: () => new Promise<void>((resolve, reject) => {
      server.close((error) => (error ? reject(error) : resolve()));
    }),
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
