install:
	pip install -r requirements.txt

test:
	python -m pytest tests/

yapf:
	find . -type f -name "*.py" | xargs yapf -i
