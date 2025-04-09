python = .venv/bin/python
pip = .venv/bin/pip

# Setup Python virtual environment and install dependencies
setup:
	python3 -m venv .venv
	$(python) -m pip install --upgrade pip
	$(pip) install -r requirements.txt

# Run the main application
run:
	$(python) main.py

# Launch the MLflow UI
mlflow:
	$(python) -m mlflow ui

# Clean cache files
clean:
	rm -rf steps/__pycache__
	rm -rf __pycache__
	rm -rf .pytest_cache

# Remove virtual environment and mlruns folder
remove:
	rm -rf .venv
	rm -rf mlruns
