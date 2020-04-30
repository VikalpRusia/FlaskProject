all: install run

install: requirement.txt
	python3 -m pip install -r requirements.txt

run: 
	export FLASK_APP=main.py
	python -m flask run
