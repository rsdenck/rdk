.PHONY: validate test

validate:
	python3 tools/validate.py && python3 tools/test_contract.py

test:
	python3 tools/test_contract.py
