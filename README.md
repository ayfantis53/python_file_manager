# File Manager Copy No Protobuf implementation (Linux)
-------------------------------------------------------------------------

## Overview

- App copies files from a data directory to a destination directory.
- Checks if files are out of date in data directory and deletes them if they don't.


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
# To Check for Errors: Use the ruff check command.
ruff check . ||  make check

# To Automatically Fix Errors:
ruff check --fix . ||  make fix

# To Format Code:
ruff format . ||  make format

# To ensure Ruff is reading the correct file and see exactly what settings are being applied:
ruff config
```


## Running Unit Tests
> When Running test copy and test retention testing suites look in `tests/test-data` for results.
> Comment out file_manage init lines `72` and `73` at current moment.
```bash
# Run in 1st terminal.          (Windows)
uv run src/utils/server.py  ||  python -m  uv run src/utils/server.py
```

```bash
# Run in 2nd terminal.

# Run all tests:                                            (Windows)
uv run pytest ||  make test                             ||  python -m  uv run pytest

# Run single test file:
uv run pytest tests/test_file_manager.py                ||  python -m  uv run pytest tests/test_file_manager.py 

# Run single test suite:
uv run pytest tests/test_file_manager.py::TestJSON      ||  python -m  uv run src/utils/server.py

# Run single test:
uv run pytest tests/test_file_manager.py::TestJSON::test_json_SUCCESS
```


## Running Code

### Running App Locally

```bash
# Run in 1st terminal.
uv run src/utils/server.py     ||  python -m  uv run src/utils/server.py

# Run in 2nd terminal.
uv run src/file_manager.py     ||  python -m  uv run src/file_manager.py 
```

### Running App with Docker

```bash
# Build container from image.
docker build -f docker/Dockerfile -t file_manager:local-build . ||  make build

# Run container from image.
docker run --rm -it --entrypoint=bash file_manager:local-build ||  make run
```

## Cleanup

```bash
# Gets rid of all directories made by python or uv.
make clean

# Get rid of built docker image
make clean-docker
```