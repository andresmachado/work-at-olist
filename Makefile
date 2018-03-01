run:
	python manage.py runserver

migrate:
	python manage.py migrate

shell:
	python manage.py shell

migrations:
	python manage.py makemigrations

requirements:
	pip install -r requirements.txt

test:
	python manage.py test --verbosity=2

build: requirements migrations migrate

clean:
	@find . -name ".DS_Store" -delete
	@find . -name "*.pyc" -delete

deploy:
	git push heroku master

migrate_heroku:
	heroku run --app=call-management python manage.py migrate