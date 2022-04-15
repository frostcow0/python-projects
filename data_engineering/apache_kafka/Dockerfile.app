# syntax=docker/dockerfile:1

FROM python:3.9-slim

WORKDIR /apache_kafka

COPY requirements.txt requirements.txt

RUN pip install -U pip
# RUN pip install -U setuptools-rust

# Update default packages
RUN apt-get update

# Get Debian packages
RUN apt-get install -y \
    gcc \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    cargo \
    librdkafka-dev

# Update new packages
RUN apt-get update

# Get Rust
# RUN curl https://sh.rustup.rs -sSf | bash -s -- -y &&
# RUN echo 'source $HOME/.cargo/env' >> $HOME/.bashrc &&

# Cryptography please cooperate
# RUN pip install --no-cache-dir cryptography

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# CMD ["python", "-m" , "flask", "run", "--host=0.0.0.0"]