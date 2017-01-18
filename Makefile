install:
	pip install -r requirements.txt

test:
	pytest

yapf:
	find . -type f -name "*.py" | xargs yapf -i
