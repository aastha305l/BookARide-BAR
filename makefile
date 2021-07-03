#name: Aastha Lamichhane
#file: makefile

.ONESHELL:
run:
	export FLASK_APP=flask_app.py
	export FLASK_ENV=development
	chrome http://127.0.0.1:5000 &
	flask run
