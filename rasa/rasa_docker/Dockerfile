FROM python:3.7-slim as base

RUN apt-get update -qq \
 && apt-get install -y --no-install-recommends \
    # required by psycopg2 at build and runtime
    libpq-dev \
     # required for health check
    curl \
 && apt-get autoremove -y

FROM base as builder

RUN apt-get update -qq && \
  apt-get install -y --no-install-recommends \
  build-essential \
  wget \
  openssh-client \
  graphviz-dev \
  pkg-config \
  git-core \
  openssl \
  libssl-dev \
  libffi6 \
  libffi-dev \
  libpng-dev

# Configure pip to use piwheels
COPY pip.conf /etc
# Download pre-built wheels for TensorFlow and TensorFlow Addons
RUN mkdir /opt/wheels/ && \
  wget -P /opt/wheels/ https://github.com/Qengineering/TensorFlow-Raspberry-Pi/raw/master/tensorflow-2.1.0-cp37-cp37m-linux_armv7l.whl && \
  wget -P /opt/wheels/ https://github.com/koenvervloesem/tensorflow-addons-on-arm/releases/download/v0.7.1/tensorflow_addons-0.7.1-cp37-cp37m-linux_armv7l.whl

# install poetry
# keep this in sync with the version in pyproject.toml and Dockerfile
ENV POETRY_VERSION 1.0.3
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH "/root/.poetry/bin:/opt/venv/bin:${PATH}"

# copy files
COPY . /build/

# change working directory
WORKDIR /build

# install dependencies
RUN python -m venv /opt/venv && \
  . /opt/venv/bin/activate && \
  pip install --no-cache-dir -U 'pip<20' && \
  poetry update --no-dev && \
  poetry install --no-dev --no-root --no-interaction && \
  poetry build -f wheel -n && \
  pip install --no-deps dist/*.whl && \
  rm -rf dist *.egg-info

# start a new build stage
FROM base as runner

# copy everything from /opt
COPY --from=builder /opt/venv /opt/venv

# Install extra dependencies
RUN apt-get install -y --no-install-recommends \
  # For numpy
  libatlas3-base libgfortran5 \
  # For matplotlib
  libfreetype6 \
  # for scikit-learn
  libgomp1 \
  # For TensorFlow Addons
  libatomic1

# make sure we use the virtualenv
ENV PATH="/opt/venv/bin:$PATH"

# update permissions & change user to not run as root
WORKDIR /app
RUN chown -R 1000:1000 /app && chmod -R g=u /app
USER 1000

# create a volume for temporary data
VOLUME /tmp

# change shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# the entry point
EXPOSE 5005
ENTRYPOINT ["rasa"]
CMD ["--help"]
