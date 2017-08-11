PYTHON := $(shell which python)
GIT := $(shell which git)
VERSION := $(shell $(PYTHON) -c "from ironman import __version__; print __version__")

clean:
	rm -rf ironman_env htmlcov
	@$(PYTHON) setup.py clean

build:
	virtualenv -p /usr/local/bin/python ironman_env && \
        source ironman_env/bin/activate && \
        pip install -r requirements.txt

coverage: clean build
        source ironman_env/bin/activate && \
        coverage run --source=ironman setup.py test && \
        coverage html && \
        coverage report

.PHONY: README.rst
README.rst:
	pandoc --from=markdown --to=rst --output=README.rst README.md
	git add README.rst
	git commit -m "update README.rst"

register:
	@$(PYTHON) setup.py register

sdist: clean
	@$(PYTHON) setup.py sdist

upload: clean
	@$(PYTHON) setup.py sdist upload

install: clean
	@$(PYTHON) setup.py install

test: install
	@$(PYTHON) setup.py test

tag:
ifeq ($(shell $(GIT) tag -l ${VERSION}),)
	$(GIT) tag -a ${VERSION} -m "${VERSION}"
else
	$(error "Already tagged version ${VERSION}")
endif
