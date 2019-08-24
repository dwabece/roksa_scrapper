test:
	PYTHONPATH=. pytest -s -vv --cov --flake8

test-cov:
	PYTHONPATH=. pytest -s -vv --cov --cov-report=html
	osascript saf.osa
