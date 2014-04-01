#
# Makefile
#

clean_pyc:
	find . -name \*.pyc -delete

install:
	bash -c 'pip install -e .'

develop:
	bash -c 'pip install -e .[develop]'

test:
	bash -c 'pip install -e .[test]'
	python setup.py test

# Convenience methods

db-init:
	manage.py db init

db-migrate:
	manage.py db migrate

db-upgrade:
	manage.py db upgrade

runserver:
	manage.py runserver

# Documentaion Helpers

docs-make:
	make -C docs clean
	make -C docs html

docs-serve: docs-make
	cd docs/_build/html && open "http://localhost:8000" && python -m SimpleHTTPServer
