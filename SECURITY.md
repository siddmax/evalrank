# Security Policy

Please report security issues privately through GitHub security advisories for this repository.

Do not file public issues, discussions, examples, or docs containing secrets, exploit details, private benchmark fixtures, held-out evaluation material, customer data, production telemetry, live project refs, or account-operation traces.

If a secret or credential is exposed, treat it as compromised, rotate or revoke it first, then coordinate history cleanup only if the residual risk still requires it.

Public ports must pass `python3 scripts/check_public_boundary.py --root .` before push. GitHub secret scanning and push protection are backstops, not approval to commit sensitive material.
