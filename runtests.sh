#!/bin/bash
echo "Running all tests and saving coverage report"
pytest -v --html=testreportdata/pytest_report.html  --self-contained-html --cov=.  --cov-report=html podcasts accounts
echo "coverage results in htmlcov/index.html"
open htmlcov/index.html
sleep 1
echo "test results in testreportdata/report.html"
open testreportdata/report.html
