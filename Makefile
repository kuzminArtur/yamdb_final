build:
	docker-compose build web

up:
	docker-compose up -d

down:
	docker-compose down

migrate:
	docker-compose exec web python manage.py migrate --noinput

createsu:
	docker-compose exec web python manage.py createsuperuser

collectstatic:
	docker-compose exec web python manage.py collectstatic --noinput

fixture:
	docker-compose exec web python manage.py loaddata fixtures.json

