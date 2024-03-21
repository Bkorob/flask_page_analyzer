install:
	poetry install

build:
	./build.sh

package-install:
	python3 -m pip install --user dist/*.whl

package-reinstall:
	python3 -m pip install --user --force-reinstall dist/*.whl

package-uninstall:
	python3 -m pip uninstall --yes dist/*.whl

dev:
	poetry run flask --app page_analyzer:app --debug run --port 7676

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

lint:
	poetry run flake8 page_analyzer

.PHONY: install build
