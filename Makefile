##
IMAGE_LABEL:=rust_env
IMAGE_TAG:=0.0.1 

##
DOCKER_CONTEXT_PATH:=./
DOCKERFILE=Dockerfile
DOCKERFILE_PATH=${DOCKER_CONTEXT_PATH}/${DOCKERFILE}

##
CONFIG_FILE_PATH=./
CONFIG_FILE_NAME=config.yaml
CONFIG_FILE=${CONFIG_FILE_PATH}/${CONFIG_FILE_NAME}

# Define the path to the yq binary, adjust as necessary
YQ=/usr/local/bin/yq

# Use shell command to read the 'host' value from the YAML and map it to Docker's platform string
HOST_ARCH:=$(shell $(YQ) e '.host' $(CONFIG_FILE))
DOCKER_PLATFORM:="linux/$(HOST_ARCH)"

# Directories for volume mounting
DEV_ENV_CONT=/etc/embedded/scripts/
DEV_ENV_HOST=/home/inumaki/Development/RustEmbeddedEnv/Docker/scripts


# New target to install yq
# Rule to install yq
install_yq:
	@echo "Installing yq..."
	@if ! command -v yq > /dev/null; then \
		sudo wget https://github.com/mikefarah/yq/releases/download/v4.27.2/yq_linux_amd64 -O $(YQ) && sudo chmod +x $(YQ); \
		echo "yq installed successfully at $(YQ)"; \
	else \
		echo "yq is already installed."; \
	fi



# Additional dependencies can be added to this rule
install: install_yq

# Modify build_docker_image to depend on the install rule
build_docker_image: install
	@echo "Building Docker image for platform $(DOCKER_PLATFORM)..."
	@docker build -t $(IMAGE_LABEL):$(IMAGE_TAG) -f $(DOCKERFILE_PATH) --platform $(DOCKER_PLATFORM) ${DOCKER_CONTEXT_PATH}

run_container:
	@sudo docker run --name ${IMAGE_LABEL} -it --privileged -v /dev/bus/usb:/dev/bus/usb ${IMAGE_LABEL}:${IMAGE_TAG}

test_run_container:
	@sudo docker run --name ${IMAGE_LABEL} -it --rm --privileged -v /dev/bus/usb:/dev/bus/usb ${IMAGE_LABEL}:${IMAGE_TAG}

start_container:
	@sudo docker start -ia ${IMAGE_LABEL} 

stop_container:
	@sudo docker stop ${IMAGE_LABEL} 

dev_run_container:
	@sudo docker run --name ${IMAGE_LABEL} -it --privileged -v /dev/bus/usb:/dev/bus/usb -v ${DEV_ENV_HOST}:${DEV_ENV_CONT} ${IMAGE_LABEL}:${IMAGE_TAG}


#stop_all_running_images:
#	@sudo docker stop $$(docker ps -aq)
#	@sudo docker rm $$(docker ps -aq)
#
#delete_untagged_images:
#	@docker rmi $$(docker images -f "dangling=true" -q)
#
#
#delete_all_images: stop_all_running_images
#	@sudo docker rmi $$(docker images -aq)

##Pass each target as a build argument and control cache usage
#docker build \
#    $CACHE_OPTION \
#    -t "${IMAGE_LABEL}:${IMAGE_TAG}" \
#    -f "${DOCKERFILE}" \
#    --platform "${PLATFORM}" \
#    --build-arg TARGETS="$TARGETS" \
#    ${CONTEXT_PATH}