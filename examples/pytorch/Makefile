create_env:
	conda create --name pytorch_test python=3.9
	
install_env:
	# conda activate pytorch_test
	conda install ipykernel pandas flake8
	pip install helpsk

env_linux: install_env
	# https://pytorch.org/get-started/locally/
	conda install pytorch torchvision torchaudio pytorch-cuda=11.7 -c pytorch -c nvidia

env_mac: install_env
	# https://pytorch.org/get-started/locally/
	conda install pytorch torchvision torchaudio -c pytorch
