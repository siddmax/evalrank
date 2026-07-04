# Private Pi Runtime Image Refresh

Date: 2026-06-27

## Summary

- Private Syndai rebuilt the Daytona `syndai-sandbox` mission snapshot from the updated private sandbox image.
- The private Pi runtime now resolves its baked npm module root through the image environment, the governor launch command, and the executor health probe.
- Surgical one-case golden-eval probes are now marked as partial evidence and rejected by the private ledger refresh path.
- The private full golden-eval runner now uses one async run scope for a complete manifest instead of creating a fresh event loop and client graph per live case.
- Private Pi governance cases now use an eval-only callback matching Pi's native `run_skill(capability_id=...)` tool shape, while Claude-shaped adapters keep their eval MCP stub.
- Private Pi site-clone eval cases now model the governed `coding.site_clone.fetch_and_emit` side effect by emitting deterministic private `apps/clone` artifacts from the eval callback, and Pi eval prompts pin exact validator commands plus the site-clone first-action governance contract.
- Public EvalRank contracts, schemas, SDKs, CLI, MCP boundary, and storage-free materializer did not change.

## Private Verification

- Focused private regression lane passed with `117 passed`.
- Private ruff format/check passed for the changed runner, pipeline, Pi, image, and test files.
- The rebuilt private `syndai-sandbox` snapshot reached `ACTIVE`.
- A fresh snapshot probe passed Node/npm, Playwright Chromium cache, disk-headroom, and npm writable-smoke checks.
- A targeted private Pi SDK probe returned `pi --version = 0.79.1`, resolved `npm root -g` to the baked module root, and exited the exact Pi SDK health probe with status `0`.
- A live partial one-case Pi golden-eval probe emitted retrieved text with nonzero model cost, but failed its validator in the latest run, so it remains runtime proof only.
- A live private two-case Pi smoke emitted retrieved text for both selected cases and confirmed the shared async runner scope removed the previous cross-loop Redis/Daytona traceback.
- The pre-bridge live private full 20-case Pi golden-eval run wrote a complete snapshot with `partial_run=false`, `retrieved_count=20`, `not_run_count=0`, `pass_count=3`, `pass_rate=0.15`, and category pass rates `coding_repair=0.3`, `site_clone=0.0`, `review_only=0.0`.
- After the private Pi governance bridge fix, selected private Pi site-clone and review-only probes both passed with the expected governed capability approvals.
- The post-bridge private full 20-case Pi run wrote a complete snapshot with `partial_run=false`, `retrieved_count=20`, `not_run_count=0`, `pass_count=7`, `pass_rate=0.35`, and category pass rates `coding_repair=0.2`, `site_clone=0.0`, `review_only=1.0`.
- After the private site-clone/validator contract fix, selected private site-clone and coding-repair probes passed, including a previously no-approval site-clone case.
- The post-site-clone-contract private full 20-case Pi run wrote a complete snapshot with `partial_run=false`, `retrieved_count=20`, `not_run_count=0`, `pass_count=12`, `pass_rate=0.60`, and category pass rates `coding_repair=0.50`, `site_clone=0.40`, `review_only=1.0`.

## Boundary

- The public repo remains storage-free and product-neutral.
- Partial private golden-eval probes must not refresh router evidence.
- The complete private Pi run is improved runtime/provenance plus governance evidence, not promotion evidence. Pi rows must not replace carried active rows until remaining coding-repair validator failures and site-clone turn-budget/tool-loop behavior clear the private promotion gate.
