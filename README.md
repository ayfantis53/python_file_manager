# File Manager Copy No Protobuf implementation
-------------------------------------------------------------------------

## Overview

- App copies files from a data directory to a destination directory.
- Checks if files are out of date in data directory and deletes them if they don't.


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

## Running Code

### Running App Locally

- To run open 2 terminals
    - Run in 1st terminal: $ python server.py
    - Run in 2nd terminal: cd app/      &&     $ python file_manager.py
- To run tests 2 terminals
    - Run in 1st terminal: $ python server.py
    - Run in 2nd terminal: cd test/      &&     $ python test_file_manager.py

- To clean out project
    - Run in terminal: cd app/      &&     $ _setup.sh  >   clean
- To build project
    - Run in terminal: $ _setup.sh  >   build

### Running App with Docker
```bash
# Build container from image.
docker build -f docker/Dockerfile -t file_manager:local-build .

# Run container from image.
docker run --rm -it --entrypoint=bash file_manager:local-build
```