FROM rust:latest as baseimage

# Use ARG to accept the targets
ARG TARGETS
#env vars
ENV ST_LINK_CLT_PATH=/opt/st/stm32cubeclt

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gdb-multiarch libnewlib-arm-none-eabi libstdc++-arm-none-eabi-newlib \
    cmake git pkg-config libusb-1.0-0-dev libudev-dev openocd \
    unzip curl wget zsh libusb-1.0.0 libusb-dev libusb-1.0.0-dev gnupg \
    libncursesw5 libncurses5-dev usbutils \
    expect tree bash-completion vim htop libreadline-dev \
    && rm -rf /var/lib/apt/lists/*

# Install the specified targets
RUN for target in $TARGETS; do \
        rustup target add $target; \
    done

# Install cargo-generate and probe-rs tools
RUN cargo install \
    cargo-generate \
    cargo-flash \
    cargo-embed \
    cargo-binutils \
    && \
    rustup component add llvm-tools-preview
 

COPY ./scripts home/.scripts
COPY ./packages home/.packages

RUN chmod +x /home/.scripts/*.sh && \
    /home/.scripts/install_stlink.sh && \
    /home/.scripts/install_stm_cube_cli.sh && \
    /home/.scripts/install_arm_toolchain.sh

# [Optional] Install any additional tools specific to STM32 CLI tools if needed
# You might need to download and install these manually depending on the tools

# [Optional] Copy your project files into the Docker container
# COPY ./your_project /workspace/your_project

# CMD or ENTRYPOINT for your build commands or to keep the container running
# For example, to build a project you might use:
# CMD ["cargo", "build", "--release", "--target=thumbv7em-none-eabihf"]