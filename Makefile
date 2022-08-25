up:
	docker compose --env-file env up --build -d

down:
	docker compose --env-file env down

sh:
	docker exec -ti loader bash

run-etl:
	docker exec loader python load_user_data.py

warehouse:
	docker exec -ti warehouse psql postgres://sfluser:sflpassword1234@localhost:5432/warehouse
