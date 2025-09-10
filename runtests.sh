#!/bin/bash
echo "Running all tests and saving coverage report"
pytest -v --html=testreportdata/pytest_report.html  --self-contained-html --cov=.  --cov-report=html podcasts accounts
echo "test results in testreportdata/report.html"
open htmlcov/index.html
open testreportdata/report.html
