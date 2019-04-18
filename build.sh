#!/usr/bin/env bash -e

# ensuring we're in virtualenv
if python -c "import sys; exit(1 if hasattr(sys, 'real_prefix') else 0)"
then
  echo 'Not in a virtual environment!'
  exit 1
fi

black -S --check .
pycodestyle .
find . -iname "*.py" -not -path "./tests/test_*" | xargs pylint
PYTHONPATH=. pytest .
