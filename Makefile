install:
	pip install django

migrate:
	python manage.py migrate

run:
	python manage.py runserver 0.0.0.0:8000

test:
	python manage.py test

fixtures:
	python manage.py loaddata leakntest/fixtures/*.yaml

lint:
	flake8 ./leakntest/*
