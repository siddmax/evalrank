# Public Release Review Closure

Closed three validated pre-release gaps without widening the public/private boundary:

- MCP HTTP destinations are configured by the host outside model-controlled tool arguments, while the Python SDK keeps explicit local and custom endpoint support with a 30-second default timeout.
- Python and TypeScript clients now fail closed on malformed or duplicate `UseCaseCatalog` responses through the portable contract validators.
- Every approved manifest right now has one linked direct-source provenance claim, including ITBench, Agents' Last Exam, and DeepSWE license sources.

Verification:

```sh
make check
```

The check passed 212 Python tests and 43 TypeScript tests on 2026-07-10.
