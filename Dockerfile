FROM python:3.10

RUN apt-get update -y && apt-get install zsh -y
RUN PATH="$PATH:/usr/bin/zsh"

RUN mkdir /code
WORKDIR /code
COPY requirements.txt .
RUN python -m pip install --upgrade pip
# RUN pip install Cython==0.29.36
# RUN pip install scikit-learn --no-build-isolation
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/code"
