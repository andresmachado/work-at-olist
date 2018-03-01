run:
	python manage.py runserver

migrate:
	python manage.py migrate

shell:
	python manage.py shell

migrations:
	python manage.py makemigrations

build: migrations migrate

clean:
	@find . -name ".DS_Store" -delete
	@find . -name "*.pyc" -delete

push_production:
	git push cbdashboard master

migrate_production:
	heroku run --app=cbdashboard python manage.py migrate