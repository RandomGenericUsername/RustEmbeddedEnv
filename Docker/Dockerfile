FROM rust:latest

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc-arm-none-eabi \
    gdb-multiarch \
    libnewlib-arm-none-eabi \
    libstdc++-arm-none-eabi-newlib \
    cmake \
    git \
    pkg-config \
    libusb-1.0-0-dev \
    libudev-dev \ 
 && rm -rf /var/lib/apt/lists/*

# Install cargo-generate and probe-rs tools
RUN cargo install cargo-generate cargo-flash cargo-embed

WORKDIR /workspace

# Use ARG to accept the targets
ARG TARGETS[]

# Install the specified targets
RUN for target in ${TARGETS[@]}; do \
        rustup target add $target; \
    done

# [Optional] Install any additional tools specific to STM32 CLI tools if needed
# You might need to download and install these manually depending on the tools

# [Optional] Copy your project files into the Docker container
# COPY ./your_project /workspace/your_project

# CMD or ENTRYPOINT for your build commands or to keep the container running
# For example, to build a project you might use:
# CMD ["cargo", "build", "--release", "--target=thumbv7em-none-eabihf"]