PROJECT_NAME = ThinkComplexity2
PYTHON_VERSION = 3.12
PYTHON_INTERPRETER = python

create_environment:
	conda create --name $(PROJECT_NAME) python=$(PYTHON_VERSION) -y
	@echo ">>> conda env created. Activate with:\nconda activate $(PROJECT_NAME)"

delete_environment:
	conda env remove --name $(PROJECT_NAME)

requirements:
	$(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt

clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

lint:
	flake8 code
	black --check --config pyproject.toml code

format:
	black --config pyproject.toml code

# Student notebooks are not tested: their exercise cells are blank, so they
# stop at the first cell that calls a function the reader is meant to write.
# One pytest run, so a failure in soln/ does not keep examples/ from running.
# nbmake runs each notebook in its own directory.
tests:
	pytest --nbmake --durations=10 soln/*.ipynb examples/*_soln.ipynb
