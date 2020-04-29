all: install

install: requirement.txt
	python3 -m pip install -r requirements.txt
