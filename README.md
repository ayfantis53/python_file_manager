# File Manager Copy
-------------------------------------------------------------------------

## Overview

- App copies files from a data directory to a destination directory.
- Checks if files are out-of-date in data directory and deletes them if they don't.


## Setup

```bash
# Install uv
pip install uv

# Install ruff
pip install ruff
```


## Formatting and Linting

### Ruff Linting
```bash
# (Linux)               (Windows)                       make
# --------------------------------------------------------------------
# To Check for Errors: Use the ruff check command.
ruff check .       ||  python -m ruff check .        ||  make check

# To Automatically Fix Errors:
ruff check --fix . ||   python -m ruff check --fix . ||  make fix

# To Format Code:
ruff format .      ||   python -m ruff format .      ||  make format

# To ensure Ruff is reading the correct file and see exactly what settings are being applied:
ruff config        ||   python -m ruff config 
```


## Running Unit Tests
> When Running test copy and test retention testing suites look in `tests/test-data` for results.

```bash
# (Linux)                       (Windows)                                 (make)
# -----------------------------------------------------------------------------------
# Run in 1st terminal.
uv run src/utils/server.py  ||  python -m  uv run src/utils/server.py   ||  make server
```

```bash
# (Linux)                                               (Windows)                            (make)
# ------------------------------------------------------------------------------------------------------------
# Run in 2nd terminal.

# Run all tests:
uv run pytest                                       ||  python -m uv run pytest         ||      make test 

# Run single test file:
uv run pytest tests/test_file_manager.py            ||  python -m uv run pytest tests/test_file_manager.py 

# Run single test suite:
uv run pytest tests/test_file_manager.py::TestJSON  ||  python -m uv run src/utils/server.py

# Run single test:
uv run pytest tests/test_file_manager.py::TestJSON::test_json_SUCCESS
```


## Running Code

### Running App Locally

> Initialize some data.
```bash
# Run in 1st terminal.
make server

# Run in 2nd terminal.
make test
```

> Now we can run our actual app
```bash
# (Linux)                           (Windows)                                 (make)
# -------------------------------------------------------------------------------------------
# Run in 1st terminal.             (Windows)
uv run src/utils/server.py     ||  python -m  uv run src/utils/server.py    || make server

# Run in 2nd terminal.                                                      (If using Ports)  (If using Protobufs)
uv run src/file_manager.py     ||  python -m  uv run src/file_manager.py    || make app     ||  make app COMM=PROTO

# Run in 3rd terminal change "isprimary".
uv run src/utils/client.py     ||  python -m  uv run src/utils/client.py    || make client PRIM=True
```

### Running App with Docker

> Get image ready.
```bash
# Build container from image.
docker build -f docker/Dockerfile -t file_manager:local-build . ||  make build

# Run container from image.
docker run --rm -it --entrypoint=bash file_manager:local-build  ||  make run
```

> Run app from image
```bash
# Find running container (use after docker run or make run command).
docker ps -a

# Open 2 new terminals.
# Enter running container through both terminals
docker exec -it $CONTAINER_ID bash

# Run each command in seperate terminals execd into running container.
make server                                         # terminal 1

make test                                           # terminal 2
make app

make client PRIM=True   ||  make client PRIM=False  # terminal 3
```


## Cleanup

```bash
# Gets rid of all directories made by python or uv.
make clean

# Get rid of built docker image
make clean-docker

# Gets rid of all directories made by python or uv & built docker image.
make clean-all
```