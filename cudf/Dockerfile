# cudf currently requires <=python3.10, and i struggled to get docker/cudf
# setup correctly using python 3.10 base image but was able to get it to work
# with `23.12-cuda12.0-py3.10` image
FROM nvcr.io/nvidia/rapidsai/base:23.12-cuda12.0-py3.10
USER root
WORKDIR /code
ENV PYTHONPATH "${PYTHONPATH}:/code"

ENV PYDEVD_WARN_EVALUATION_TIMEOUT 1000

RUN apt-get update -y 
#&& apt-get install zsh -y
RUN PATH="$PATH:/usr/bin/zsh"

RUN apt-get install lsof

RUN python -m pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt

RUN pip install torch

# install cudf
RUN pip install \
    --extra-index-url=https://pypi.nvidia.com \
    cudf-cu12==23.12.* dask-cudf-cu12==23.12.* cuml-cu12==23.12.* \
    cugraph-cu12==23.12.* cuspatial-cu12==23.12.* cuproj-cu12==23.12.* \
    cuxfilter-cu12==23.12.* cucim-cu12==23.12.* pylibraft-cu12==23.12.* \
    raft-dask-cu12==23.12.*
