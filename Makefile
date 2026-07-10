.PHONY: check

TS_DEPS_STAMP := packages/sdk-ts/node_modules/.package-lock.json

$(TS_DEPS_STAMP): packages/sdk-ts/package.json packages/sdk-ts/package-lock.json
	npm ci --prefix packages/sdk-ts

check: $(TS_DEPS_STAMP)
	python3 scripts/check_public_boundary.py --root .
	python3 -m unittest discover tests
	npm run check --prefix packages/sdk-ts
	npm run test --prefix packages/sdk-ts
