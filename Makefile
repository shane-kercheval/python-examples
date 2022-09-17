conda_env_name = python_examples

####
# DOCKER
####
docker_compose:
	# docker build -t data-science-template .
	docker compose -f docker-compose.yml up --build

docker_run: notebook zsh

notebook:
	open 'http://127.0.0.1:8888/?token=d4484563805c48c9b55f75eb8b28b3797c6757ad4871776d'

zsh:
	docker exec -it python-examples-bash-1 /bin/zsh

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

