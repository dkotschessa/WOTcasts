echo "Running all tests and saving coverage report"
pytest --cov=.  --cov-report=html podcasts
open htmlcov/index.html
