create_env:
	# https://pytorch.org/get-started/locally/
	conda create --name pytorch_test python=3.9

env_linux: create_env
	conda install pytorch torchvision torchaudio pytorch-cuda=11.7 -c pytorch -c nvidia

env_mac: create_env
	# https://pytorch.org/get-started/locally/
	conda install pytorch torchvision torchaudio -c pytorch
	conda activate pytorch_test
