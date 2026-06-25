# Contributing

EvalRank accepts changes that keep the public core product-neutral and independently testable.

Before opening a pull request, run:

```sh
python3 scripts/check_public_boundary.py --root .
python3 -m unittest discover tests
```

Do not add private Syndai imports, secrets, held-out fixtures, or hosted-product-only behavior to public packages.
