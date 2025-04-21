# Makefile

dev:
	docker compose up -d

prod:
	docker compose -f docker-compose.yml up -d --build

down:
	docker compose down

logs:
	docker compose logs -f

restart-backend:
	docker compose restart backend

restart-frontend:
	docker compose restart frontend

init-db:
	docker compose exec backend python app/init_db.py

setup:
	@if docker compose ps --services --filter "status=running" | grep -q backend; then \
		echo "[✔] Containers already running. Skipping make dev."; \
	else \
		echo "[*] Containers not running. Starting dev environment..."; \
		make dev; \
	fi
	make init-db


rebuild:
	make down
	@if [ -d backend/users.db ]; then \
		echo "[*] Removing broken users.db folder..."; \
		rm -rf backend/users.db; \
	fi
	@if [ -f backend/users.db ]; then \
		echo "[*] Removing old users.db file..."; \
		rm -f backend/users.db; \
	fi
	make dev
	make init-db

build:
	docker compose up -d --build
	@echo "[*] Building the Docker images..."

clean:
	@echo "[*] Stopping and removing all containers and networks..."
	-docker compose down --volumes --remove-orphans
	@echo "[*] Removing dangling images..."
	-docker image prune -f
	@echo "[*] Removing dangling volumes..."
	-docker volume prune -f

doctor:
	@echo "[*] Checking Docker daemon status..."
	@if ! docker info > /dev/null 2>&1; then \
		echo "[✖] Docker is not running! Start Docker Desktop or service first."; \
		exit 1; \
	else \
		echo "[✔] Docker is running."; \
	fi

	@echo "[*] Checking Docker Compose installation..."
	@if ! docker compose version > /dev/null 2>&1; then \
		echo "[✖] Docker Compose is not installed correctly."; \
		exit 1; \
	else \
		echo "[✔] Docker Compose is installed."; \
	fi

	@echo "[*] Checking backend Dockerfile..."
	@if [ ! -f backend/Dockerfile ]; then \
		echo "[✖] Missing backend/Dockerfile!"; \
		exit 1; \
	else \
		echo "[✔] Backend Dockerfile found."; \
	fi

	@echo "[*] Checking frontend Dockerfile..."
	@if [ ! -f frontend/Dockerfile ]; then \
		echo "[✖] Missing frontend/Dockerfile!"; \
		exit 1; \
	else \
		echo "[✔] Frontend Dockerfile found."; \
	fi

	@echo "[✔] Environment looks good! Ready to develop. 🚀"

deploy:
	@echo "[*] Building images for production..."
	docker compose -f docker-compose.yml -f docker-compose.prod.yml build

	@echo "[*] Tagging backend and frontend images..."
	docker tag ordersys-backend yourdockerhubusername/ordersys-backend:latest
	docker tag ordersys-frontend yourdockerhubusername/ordersys-frontend:latest

	@echo "[*] Pushing images to Docker Hub..."
	docker push yourdockerhubusername/ordersys-backend:latest
	docker push yourdockerhubusername/ordersys-frontend:latest

	@echo "[*] Deployment build and push complete! Ready to deploy remotely."
