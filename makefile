all: install run

install: requirement.txt
	python3 -m pip install -r requirements.txt

run: 
	export FLASK_APP=main.py
	python3 -m flask run
	xdg-open "http://127.0.0.1:5000/"
