# Tests Agent Guide

## Scope

- Public unit and boundary tests live here.

## Rules

- Use stdlib `unittest` unless the repo deliberately adopts another test runner.
- Keep fixtures inline, tiny, and public.
- Tests must not require network access, private credentials, private repos, or private data.

## Checks

- From repo root: `python3 -m unittest discover tests`
