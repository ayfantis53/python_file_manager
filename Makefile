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


# ===========
# TARGETS.
# ===========

# --- Utility Targets ---

# linting.
check:
	ruff check .
fix:
	ruff check --fix .
format:
	ruff format .

# testing.
test:
	uv run pytest
# Run App.
run:
	docker run --rm -it --entrypoint=bash file_manager:${TAG}

# --- Build Targets ---
build:
	docker build -f docker/Dockerfile -t file_manager:${TAG} .


# ===========
# MAINTENANCE.
# ===========

# .PHONY tells Make that 'clean' is not a physical file.
.PHONY: clean help

# Clean up build artifacts.
clean:
	rm -rf .ruff_cache .pytest_cache .venv tests/__pycache__ /src/file_manager.egg-info tests/test_data/ src/__pycache__ src/file_manager.egg-info src/modules/__pycache__
# Clean up docker.
clean-docker:
	docker rmi file_manager:${TAG}

# Self-documenting help target.
help:
	@grep -E '^[a-z.A-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST)  | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'
