install:
	pip install --upgrade pip &&\
		pip3 install -r requirements.txt

format:
	black *.py

lint:
	pylint --disable=R,C main.py

#test:
#	python3 -m pytest -vv test.py

all: install format lint