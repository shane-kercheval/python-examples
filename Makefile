conda_env_name = python_examples

####
# DOCKER
####
docker_build:
	# docker build -t data-science-template .
	docker compose -f docker-compose.yml up --build

docker_run: docker_build
	# run the docker container
	docker compose -f docker-compose.yml up

docker_down:
	docker compose down --remove-orphans

docker_rebuild:
	docker compose -f docker-compose.yml build --no-cache

docker_zsh:
	# run container and open up zsh command-line
	docker exec -it python-helpers-bash-1 /bin/zsh

####
# Conda
####
# conda activate python_examples
env:
	conda env create -f environment.yml

export_env:
	conda env export > environment.yml	

remove_env:
	conda env remove -n $(conda_env_name)

####
# Project
####
linting:
	flake8 --max-line-length 110 .

run:
	python main.py

