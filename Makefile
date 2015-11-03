clean:
	rm -rf ironman_env htmlcov

build:
	virtualenv -p /usr/local/bin/python ironman_env && \
        source ironman_env/bin/activate && \
        pip install -r requirements.txt

test: clean build
        source ironman_env/bin/activate && \
        coverage run --source=ironman setup.py test && \
        coverage html && \
        coverage report

.PHONY: README.rst
README.rst:
	pandoc --from=markdown --to=rst --output=README.rst README.md
	git stash
	git add README.rst
	git commit -m "update README.rst"
	git stash pop
