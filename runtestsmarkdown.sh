#!/bin/bash
echo "Running all tests and saving coverage report"
#pytest -v --md-report  --self-contained-html --cov=.  --cov-report=markdown podcasts accounts
pytest --cov-report markdown
echo "test results in testreportdata/report.html"
