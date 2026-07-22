# Contributing

EvalRank accepts changes that keep the public core product-neutral and independently testable.

Before opening a pull request, run:

```sh
python3 scripts/check_public_boundary.py --root .
python3 -m unittest discover tests
```

Do not add private imports, secrets, private fixtures, or hosted-product-only behavior to public packages. Runtime persistence and hosted operation are maintained in a separate private system.

Keep `AGENTS.md` and the nearest scoped `AGENTS.md` current when ownership, commands, or package boundaries change. Add or update `TESTS.md` when test commands change, and add `NAVIGATION.md` only when UI routes, API routes, or deeplinks exist.
