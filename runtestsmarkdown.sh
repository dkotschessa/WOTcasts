#!/bin/bash
echo "Running all tests and saving coverage report"
pytest --md-report  --self-contained-html --cov=.  podcasts accounts
coverage report --format=markdown
#echo "test results in testreportdata/report.html"
