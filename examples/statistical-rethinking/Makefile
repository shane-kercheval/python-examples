.PHONY: tests

####
# DOCKER
####
docker_build:
	docker compose -f docker-compose.yml build

docker_run: docker_build
	docker compose -f docker-compose.yml up

docker_down:
	docker compose down --remove-orphans

docker_rebuild:
	docker compose -f docker-compose.yml build --no-cache

docker_bash:
	docker compose -f docker-compose.yml up --build bash

docker_open: notebook mlflow_ui zsh

notebook:
	open 'http://127.0.0.1:8888/?token=d4484563805c48c9b55f75eb8b28b3797c6757ad4871776d'

zsh:
	docker exec -it statistical-rethinking-bash-1 /bin/zsh

####
# Project
####
linting:
	flake8 --max-line-length 99 .

tests: linting
	pytest tests/

chapter_1:
	jupyter nbconvert --execute --to html notebooks/chapter-1.ipynb
	mv notebooks/chapter-1.html output/chapter-1.html

all: chapter_1
