FROM rust:latest as base-image-dependencies


### env vars
#ENV ST_LINK_CLT_PATH=/opt/st/stm32cubeclt
ENV PACKAGES_DIR=/etc/embedded/packages
ENV SCRIPTS_DIR=/etc/embedded/scripts
ENV PYTHON_REQUIREMENTS=/etc/embedded/requirements/python_requirements.txt
ENV USER=root
ENV PYTHON_VENV_PATH=/opt/venv
ENV PYTHON_PIP=$PYTHON_VENV_PATH/bin/pip
ENV PYTHON=$PYTHON_VENV_PATH/bin/python3

### Install system dependencies
RUN apt-get update && apt-get install -y \
    cmake git curl wget pkg-config unzip zsh build-essential gnupg gdb-multiarch openocd \
    libusb-1.0-0-dev libudev-dev libusb-1.0.0 libusb-dev libreadline-dev \
    libncursesw5 libncurses5-dev libusb-1.0.0-dev usbutils  \
    python3 python3-pip python3-venv \
    libnewlib-arm-none-eabi libstdc++-arm-none-eabi-newlib \
    expect tree bash-completion vim htop  \
    && rm -rf /var/lib/apt/lists/*

### Install cargo-generate and probe-rs tools
RUN cargo install \
    cargo-generate \
    cargo-flash \
    cargo-embed \
    cargo-binutils \
    && \
    rustup component add llvm-tools-preview

FROM base-image-dependencies as config-scripts 

###
COPY ./Docker/scripts $SCRIPTS_DIR 
COPY ./Docker/packages $PACKAGES_DIR 
COPY ./Docker/scripts/python_requirements.txt $PYTHON_REQUIREMENTS 

# create venv for python
RUN python3 -m venv $PYTHON_VENV_PATH && \
    $PYTHON_PIP install -r $PYTHON_REQUIREMENTS

RUN chmod +x $SCRIPTS_DIR/*.sh && \
    $SCRIPTS_DIR/install_stlink.sh && \
    $SCRIPTS_DIR/install_stm_cube_cli.sh
    #ln -s $SCRIPTS_DIR/create_project.py /usr/local/bin/create_project











# [Optional] Install any additional tools specific to STM32 CLI tools if needed
# You might need to download and install these manually depending on the tools

# [Optional] Copy your project files into the Docker container
# COPY ./your_project /workspace/your_project

# CMD or ENTRYPOINT for your build commands or to keep the container running
# For example, to build a project you might use:
# CMD ["cargo", "build", "--release", "--target=thumbv7em-none-eabihf"]