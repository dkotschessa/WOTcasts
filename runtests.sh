#!/bin/bash
echo "Running all tests and saving coverage report"
pytest -v --cov=.  --cov-report=html podcasts accounts
open htmlcov/index.html
