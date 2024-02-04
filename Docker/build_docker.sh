#!/bin/sh

# Determine the directory where this script is located
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

# Default values
TARGETS_CONFIG="${SCRIPT_DIR}/targets.config"
DOCKERFILE="${SCRIPT_DIR}/Dockerfile"
IMAGE_LABEL=""
IMAGE_TAG=""
PLATFORM="linux/x86_64"
CACHE_OPTION=""
CONTEXT_PATH="${SCRIPT_DIR}"

# Display help message
show_help() {
    echo "Usage: $0 -L <image-label> -T <image-tag> [options]"
    echo ""
    echo "Mandatory options:"
    echo "  -L, --image-label    Specify the Docker image label"
    echo "  -T, --image-tag      Specify the Docker image tag"
    echo ""
    echo "Optional options:"
    echo "  --targets-config     Path to the targets configuration file (default: same directory as build_docker.sh)"
    echo "  -f, --dockerfile     Path to the Dockerfile (default: Dockerfile)"
    echo "  --platform           Specify the build platform (default: linux/amd64)"
    echo "  --no-cache           Build without using Docker's cache"
    echo ""
    echo "  -h, --help           Display this help message"
    echo ""
    echo "This script builds a Docker image for STM32 development with specified options."
}

# Function to parse command-line options
parse_args() {
    if [ $# -eq 0 ]; then
        show_help
        exit 1
    fi

    while [ "$#" -gt 0 ]; do
        case $1 in
            -h|--help) show_help; exit 0 ;;
            -L|--image-label) IMAGE_LABEL="$2"; shift ;;
            -T|--image-tag) IMAGE_TAG="$2"; shift ;;
            --targets-config) TARGETS_CONFIG="$2"; shift ;;
            -f|--dockerfile) DOCKERFILE="$2"; shift ;;
            --context) CONTEXT_PATH="$2"; shift ;;
            --platform) PLATFORM="$2"; shift ;;
            --no-cache) CACHE_OPTION="--no-cache" ;;
            *) echo "Unknown parameter passed: $1"; exit 1 ;;
        esac
        shift
    done

    # Check if mandatory options are set
    if [ -z "$IMAGE_LABEL" ]; then
        echo "Error: Image label is mandatory."
        show_help
        exit 1
    fi

    if [ -z "$IMAGE_TAG" ]; then
        echo "Error: Image tag is mandatory."
        show_help
        exit 1
    fi
}

parse_args "$@"

# Read targets from the configuration file
TARGETS=$(cat "$TARGETS_CONFIG" | xargs)

#Pass each target as a build argument and control cache usage
docker build \
    $CACHE_OPTION \
    -t "${IMAGE_LABEL}:${IMAGE_TAG}" \
    -f "${DOCKERFILE}" \
    --platform "${PLATFORM}" \
    --build-arg TARGETS="$TARGETS" \
    ${CONTEXT_PATH}

