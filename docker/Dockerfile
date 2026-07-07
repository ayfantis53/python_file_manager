############################################################################################                              
#
#   _____ _ _            __  __                                   
#  |  ___(_) | ___      |  \/  | __ _ _ __   __ _  __ _  ___ _ __ 
#  | |_  | | |/ _ \_____| |\/| |/ _` | '_ \ / _` |/ _` |/ _ \ '__|
#  |  _| | | |  __/_____| |  | | (_| | | | | (_| | (_| |  __/ |   
#  |_|   |_|_|\___|     |_|  |_|\__,_|_| |_|\__,_|\__, |\___|_|   
#                                                 |___/             
#
#
# FILE-MANAGER
#
# https://github.com/ayfantis53/python_file_manager

ARG PYTHON_VERSION="3.12"
ARG BUILD_IMAGE="redhat/ubi9:latest"

############################################################################################
# file-manager layer.
# This is a MINIMAL RUNTIME image with all installs needed for file-manager image.
# For building file-manager using applications.
############################################################################################

# Use the file-manager-image as the foundation base image.
FROM ${BUILD_IMAGE} AS file-manager


# =========
# Setup.
# =========

# switch the administrative context of a container to the superusers.
USER root

# Prevent Encoding Crashes: Python 3 and other languages may throw a UnicodeEncodeError when they encounter a non-ASCII character.
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
# prepends the Python virtual environment's binary folder to the system PATH.
# ensures any subsequent commands (like python or pip) run within that environment, 
# automatically using the packages installed there without needing to run source venv/bin/activate. 
ENV PATH="/opt/app-build/.venv/bin:$PATH"
# forces the Astral uv package manager to copy files instead of creating hard links when installing dependencies.
# used to eliminate warnings and errors when using Docker BuildKit cache mounts as hard links cannot span across different file systems.
ENV UV_LINK_MODE=copy
# Set a writable cache location in Docker.
# Redirect uv to write to directories owned by the user.
ENV UV_PYTHON_INSTALL_DIR=/tmp/uv/python
ENV UV_CACHE_DIR=/tmp/uv/cache

# Set the working directory.
WORKDIR /opt/app/

# copy over because we need to run file_manager.
COPY conf /opt/app/conf
COPY src /opt/app/src
COPY tests /opt/app/tests
COPY pyproject.toml uv.lock Makefile /opt/app/


# =========
# Installs.
# =========

# Install behave compiler and development libraries.
RUN dnf install -v --setopt=install_weak_deps=False -y --nogpgcheck \
        make \
        python${PYTHON_VERSION} \
        python${PYTHON_VERSION}-devel \
        python${PYTHON_VERSION}-pip \
        protobuf \
        protobuf-compiler \
        gcc-c++ \
    # Cleanup.
    && dnf -q clean all \
    && rm -rf /var/cache/dnf/* \
    && rm /etc/yum.repos.d/*

# Install uv.
RUN pip install --upgrade pip && pip install protobuf \
    && pip install uv \
    # Remove ubi-9 python garbage
    && rm -f /usr/local/lib/python3.11/ensurepip/_bundled/setuptools-65.5.0-py3-none-any.whl


# =========
# Permission fix
# =========

# Create the application directory and set ownership to your user (UID 1000).
RUN mkdir -p /opt/app && chown -R 1000:1000 /opt/app
RUN mkdir -p /tmp/uv-cache && chown -R 1000:1000 /tmp/uv-cache
# Switch to the non-privileged user for subsequent commands.
USER 1000
# Now you can create the virtual environment without permission issues.
WORKDIR /opt/app


# =========
# Finish setup.
# =========

# Verify installation.
RUN uv --version \
    && protoc --version \
    && uv pip show protobuf

# dump a Python traceback to standard error (stderr) when a fatal crash occurs, such as a segmentation fault (segfault).
ENV PYTHONFAULTHANDLER=1

# overrides the default signal sent to a container when it is stopped via docker stop.
STOPSIGNAL SIGINT

# configures a container to run as an executable, specifically launching the Python interpreter 
# to execute a script named evaluate_messages.py immediately upon startup. 
ENTRYPOINT ["uv", "run", "src/file_manager.py"]