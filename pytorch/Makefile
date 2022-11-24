create_env:
	conda create --name pytorch_test python=3.9
	conda activate pytorch_test
	conda install ipykernel

env_linux: create_env
	# https://pytorch.org/get-started/locally/
	conda install pytorch torchvision torchaudio pytorch-cuda=11.7 -c pytorch -c nvidia

env_mac: create_env
	# https://pytorch.org/get-started/locally/
	conda install pytorch torchvision torchaudio -c pytorch
