#####################################################################
#					 **File-Manager Makefile **						
# 
# @description: This Makefile can build a File-Manager image,
#					pull a File-Manager image, & cleanup repo 
#					of all untracked files/folders.
# @last-modified: 2026-06-06
#####################################################################

# ===========
# PROJECT VARIABLES
# ===========

TAG?="local-build"


# ===========
# TARGETS
# ===========

# --- Utility Targets ---

# linting.
check:
	ruff check .
fix:
	ruff check --fix .
format:
	ruff format .

# testing
test:
	uv run pytest

# Run App.
up:
	TAG=${TAG}
down:
	TAG=${TAG}

# --- Build Targets ---
build:
	TAG=${TAG}


# ===========
# MAINTENANCE
# ===========

# .PHONY tells Make that 'clean' is not a physical file
.PHONY: clean help

# Clean up build artifacts
clean:
	rm -rf .ruff_cache python_file_manager/.pytest_cache python_file_manager/.venv python_file_manager/tests/__pycache__ python_file_manager/src/file_manager.egg-info

# Self-documenting help target 
help:
	@grep -E '^[a-z.A-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST)  | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'
