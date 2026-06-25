.PHONY: check

check:
	python3 scripts/check_public_boundary.py --root .
	python3 -m unittest discover tests
