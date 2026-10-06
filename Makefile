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
# soln/ holds the canonical copies of the shared modules; the others are copies.
# notebooks/ copies are what notebooks download from GitHub, so they have to be
# real files, not links.  examples/utils.py is a copy too, but not tracked.
SHARED = utils.py Cell2D.py
COPIES = $(foreach d,notebooks code,$(addprefix $(d)/,$(SHARED)))

sync-shared:
	for f in $(COPIES); do cp soln/$$(basename $$f) $$f; done
	cp soln/utils.py examples/utils.py

# Fails if a tracked copy is out of date.
check-shared:
	@for f in $(COPIES); do \
		cmp -s soln/$$(basename $$f) $$f || { echo "$$f is out of date: run make sync-shared"; exit 1; }; \
	done

# One pytest run, so a failure in soln/ does not keep examples/ from running.
# nbmake runs each notebook in its own directory.
tests: check-shared
	pytest --nbmake --durations=10 soln/*.ipynb examples/*_soln.ipynb
