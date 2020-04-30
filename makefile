all: install run

install: requirement.txt
	python3 -m pip install -r requirements.txt

run: 
	export FLASK_APP=main.py
	python3 -m flask run
	python3 -m webbrowser http://127.0.0.1:5000/
