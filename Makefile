#####################################################################
#					 **File-Manager Makefile **						
# 
# @description: This Makefile can build a File-Manager image,
#					pull a File-Manager image, & cleanup repo 
#					of all untracked files/folders.
# @last-modified: 2026-06-06
#####################################################################

# ===========
# PROJECT VARIABLES.
# ===========

TAG?="local-build"
PRIM="true"
JSON=./conf/file_manager.conf
COMM=PORT

# --- Setup OS ---

# If Windows need python -m prefix.
ifeq ($(OS), Windows_NT)
    OS_PRE = python -m 
# If Linux not needed.
else
	OS_PRE?=""
endif


# ===========
# TARGETS.
# ===========

# --- Utility Targets ---

# linting.
check:
	${OS_PRE}ruff check .
fix:
	${OS_PRE}ruff check --fix .
format:
	${OS_PRE}ruff format .

# testing.
app:
	${OS_PRE}uv run src/file_manager.py --json-file $(JSON) --comms $(COMM)
client:
	${OS_PRE}uv run src/utils/client.py $(PRIM)
server:
	${OS_PRE}uv run src/utils/server.py
test:
	${OS_PRE}uv run pytest


# --- Build Docker ---
# Build Docker Image.
build:
	docker build -f docker/Dockerfile -t file_manager:${TAG} .
# Run Docker Image.
run:
	docker run --rm -it --entrypoint=bash file_manager:${TAG}


# ===========
# MAINTENANCE.
# ===========

# .PHONY tells Make that 'clean' is not a physical file.
.PHONY: clean clean-docker help

# Clean up build artifacts.
clean:
	rm -rf \
		.ruff_cache \
		.pytest_cache \
		.venv tests/__pycache__ \
		/src/file_manager.egg-info \
		tests/test_data/ \
		src/__pycache__ \
		src/file_manager.egg-info \
		src/modules/__pycache__ \
		**log* \
	&& clear
# Clean up docker.
clean-docker:
	docker rmi file_manager:${TAG}

# Self-documenting help target.
help:
	@grep -E '^[a-z.A-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST)  | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'
