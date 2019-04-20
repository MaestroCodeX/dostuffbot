run:
	python3 dostuffbot/manage.py run_main

migrations:
	python3 dostuffbot/manage.py makemigrations

migrate:
	python3 dostuffbot/manage.py migrate

messages:
	python3 dostuffbot/manage.py makemessages -l $(lang)

compilemessages:
	python3 dostuffbot/manage.py compilemessages

run-bot:
	python3 dostuffbot/manage.py run_bot
