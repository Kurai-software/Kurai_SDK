.PHONY: help install install-dev test lint clean build upload upload-test

help:
	@echo "Comandos disponibles para Kurai SDK:"
	@echo "  install      - Instalar el paquete localmente"
	@echo "  install-dev  - Instalar dependencias de desarrollo"
	@echo "  test         - Ejecutar tests"
	@echo "  lint         - Ejecutar linting y formateo"
	@echo "  clean        - Limpiar archivos de build"
	@echo "  build        - Construir paquete para distribución"
	@echo "  upload-test  - Subir a TestPyPI"
	@echo "  upload       - Subir a PyPI"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

test:
	python -m pytest tests/ -v

lint:
	python -m black kurai tests examples
	python -m flake8 kurai tests examples
	python -m mypy kurai

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean lint
	python -m build

upload-test: build
	python -m twine upload --repository testpypi dist/*

upload: build
	python -m twine upload dist/*

check:
	python -m twine check dist/*
	python setup.py check --strict --metadata