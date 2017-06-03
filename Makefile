install:
	pip install django; \
	pip install pyyaml; \
  pip install selenium; \
  pip install flake8; \
	wget https://github.com/mozilla/geckodriver/releases/download/v0.16.1/geckodriver-v0.16.1-linux64.tar.gz; \
  mkdir geckodriver; \
  tar -xzf geckodriver-v0.16.1-linux64.tar.gz -C geckodriver; \
  export PATH=$PATH:$PWD/geckodriver

migrate:
	python manage.py migrate

run:
	python manage.py runserver 0.0.0.0:8000

test:
	coverage run --source=leakntest manage.py test

fixtures:
	python manage.py loaddata leakntest/fixtures/*.yaml

lint:
	flake8 ./leakntest/*
