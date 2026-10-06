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
# soln/utils.py is canonical; the others are copies.  notebooks/utils.py is
# the one notebooks download from GitHub, so it has to be a real file, not a link.
UTILS_COPIES = notebooks/utils.py code/utils.py examples/utils.py

sync-utils:
	for f in $(UTILS_COPIES); do cp soln/utils.py $$f; done

# Fails if a tracked copy is out of date (examples/utils.py is not tracked).
check-utils:
	@for f in notebooks/utils.py code/utils.py; do \
		cmp -s soln/utils.py $$f || { echo "$$f is out of date: run make sync-utils"; exit 1; }; \
	done

# One pytest run, so a failure in soln/ does not keep examples/ from running.
# nbmake runs each notebook in its own directory.
tests: check-utils
	pytest --nbmake --durations=10 soln/*.ipynb examples/*_soln.ipynb
