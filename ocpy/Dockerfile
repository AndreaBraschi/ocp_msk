FROM ubuntu:22.04

# install git, but first update packages and remove the list of those that are recommended.
# We need git so that we can use it to git clone one of the dependencies in the pyproject.toml file. 
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential ca-certificates git \
    && rm -rf /var/lib/apt/lists/*

# copy paths of project dir in the image
COPY . /ocpy

# download uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# instructions to activate environment
ENV VIRTUAL_ENV=/ocpy/.venv \
    PATH="ocpy/.venv/bin:$PATH" \
    UV_LINK_MODE=copy

# create a uv env with a version of python and activate the environment
RUN uv venv --python 3.13.13 "$VIRTUAL_ENV"

# install package dependencies.
RUN uv pip install -v /ocpy
