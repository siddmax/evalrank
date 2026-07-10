/** Portable identities for one immutable EvalRank aggregation input. */

import {
  MAX_SAFE_INTEGER,
  canonicalJson,
  sha256Hex,
} from "./decision-contracts.ts";


const digestPattern = /^[0-9a-f]{64}$/;
const calibrationReportIdPattern = /^calibration_[0-9a-f]{64}$/;
const observationIdPattern = /^obs_[0-9a-f]{64}$/;
const aggregationDocumentKeys = [
  "admission_cohort_digest",
  "calibration_report_id",
  "methodology_version",
  "observation_ids",
  "ranking_group",
] as const;

export type RankingGroupIdentity = readonly [string, string, string, string];

export interface AggregationInputDocument {
  admission_cohort_digest: string;
  calibration_report_id: string;
  methodology_version: string;
  observation_ids: string[];
  ranking_group: RankingGroupIdentity;
}

export interface BootstrapSeedDocument {
  aggregation_input_digest: string;
  methodology_version: string;
}

export function aggregationInputDocument(value: unknown): AggregationInputDocument {
  const payload = exactAggregationDocument(value);
  const document: AggregationInputDocument = {
    admission_cohort_digest: patternString(
      payload.admission_cohort_digest,
      digestPattern,
      "admission_cohort_digest",
    ),
    calibration_report_id: patternString(
      payload.calibration_report_id,
      calibrationReportIdPattern,
      "calibration_report_id",
    ),
    methodology_version: nonEmptyString(
      payload.methodology_version,
      "methodology_version",
    ),
    observation_ids: observationIds(payload.observation_ids),
    ranking_group: rankingGroup(payload.ranking_group),
  };
  canonicalJson(document);
  return document;
}

export async function deriveAggregationInputDigest(value: unknown): Promise<string> {
  return sha256Hex(aggregationInputDocument(value));
}

export function bootstrapSeedDocument(
  aggregationInputDigest: unknown,
  methodologyVersion: unknown,
): BootstrapSeedDocument {
  const document = {
    aggregation_input_digest: patternString(
      aggregationInputDigest,
      digestPattern,
      "aggregation_input_digest",
    ),
    methodology_version: nonEmptyString(methodologyVersion, "methodology_version"),
  };
  canonicalJson(document);
  return document;
}

export async function deriveBootstrapSeed(
  aggregationInputDigest: unknown,
  methodologyVersion: unknown,
): Promise<number> {
  const digest = await sha256Hex(
    bootstrapSeedDocument(aggregationInputDigest, methodologyVersion),
  );
  const firstEightBytes = BigInt(`0x${digest.slice(0, 16)}`);
  return Number(firstEightBytes & BigInt(MAX_SAFE_INTEGER));
}

function exactAggregationDocument(value: unknown): Record<string, unknown> {
  if (typeof value !== "object" || value === null || Array.isArray(value)) {
    throw new TypeError("aggregation input must be an object");
  }
  const payload = value as Record<string, unknown>;
  const actualKeys = Object.keys(payload).sort();
  const expectedKeys = [...aggregationDocumentKeys].sort();
  if (
    actualKeys.length !== expectedKeys.length
    || actualKeys.some((key, index) => key !== expectedKeys[index])
  ) {
    throw new TypeError("aggregation input must contain exactly the documented fields");
  }
  return payload;
}

function observationIds(value: unknown): string[] {
  if (!Array.isArray(value)) {
    throw new TypeError("observation_ids must be an array");
  }
  if (value.length === 0) {
    throw new TypeError("observation_ids must be non-empty");
  }
  for (let index = 0; index < value.length; index += 1) {
    if (!(index in value)) throw new TypeError("observation_ids must not be sparse");
  }
  const observations = value.map((item) =>
    patternString(item, observationIdPattern, "observation_ids item")
  );
  if (new Set(observations).size !== observations.length) {
    throw new TypeError("observation_ids must be unique");
  }
  return [...observations].sort();
}

function rankingGroup(value: unknown): RankingGroupIdentity {
  if (!Array.isArray(value)) {
    throw new TypeError("ranking_group must be an array");
  }
  if (value.length !== 4) {
    throw new TypeError("ranking_group must contain exactly four strings");
  }
  for (let index = 0; index < value.length; index += 1) {
    if (!(index in value)) throw new TypeError("ranking_group must not be sparse");
  }
  const group = value.map((item, index) =>
    nonEmptyString(item, `ranking_group[${index}]`)
  );
  return group as [string, string, string, string];
}

function patternString(value: unknown, pattern: RegExp, name: string): string {
  if (typeof value !== "string") {
    throw new TypeError(`${name} must be a string`);
  }
  if (!pattern.test(value)) {
    throw new TypeError(`${name} has an invalid format`);
  }
  return value;
}

function nonEmptyString(value: unknown, name: string): string {
  if (typeof value !== "string" || value.length === 0) {
    throw new TypeError(`${name} must be a non-empty string`);
  }
  return value;
}
