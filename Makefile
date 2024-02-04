##
IMAGE_LABEL:=rust_env
IMAGE_TAG:=0.0.1 

##
DOCKER_PATH:=./Docker
DOCKER_BUILD_SCRIPT:=build_docker.sh
DOCKER_BUILD_SCRIPT_PATH:=${DOCKER_PATH}/${DOCKER_BUILD_SCRIPT}

#Target machine
OS:=linux
ARCH:=x86_64
PLATFORM:=${OS}/${ARCH}

build_docker_image:
	@bash $(DOCKER_BUILD_SCRIPT_PATH) -L ${IMAGE_LABEL} -T ${IMAGE_TAG} --platform ${PLATFORM} --context ${DOCKER_PATH}

build_docker_image_no_cache:
	@bash $(DOCKER_BUILD_SCRIPT_PATH) -L ${IMAGE_LABEL} -T ${IMAGE_TAG} --platform ${PLATFORM} --context ${DOCKER_PATH} --no-cache

run_container:
	@sudo docker run --name ${IMAGE_LABEL} -it --privileged -v /dev/bus/usb:/dev/bus/usb ${IMAGE_LABEL}:${IMAGE_TAG}

start_container:
	@sudo docker start -ia ${IMAGE_LABEL} 
	
stop_all_running_images:
	@sudo docker stop $$(docker ps -aq)
	@sudo docker rm $$(docker ps -aq)

delete_untagged_images:
	@docker rmi $$(docker images -f "dangling=true" -q)


delete_all_images: stop_all_running_images
	@sudo docker rmi $$(docker images -aq)
