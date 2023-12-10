IMAGE_NAME = post_code_validator
IMAGE_TAG = latest

.PHONY: build start stop logs rm

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .

# Start or run the Docker container
start:
	docker start -a $(IMAGE_NAME) || docker run -p 3500:3500 -it --name=$(IMAGE_NAME) $(IMAGE_NAME):$(IMAGE_TAG)

# Stop the Docker container
stop:
	docker stop $(IMAGE_NAME)

# Check the logs of the Docker container
logs:
	docker logs $(IMAGE_NAME)

# Remove the Docker container
rm:
	docker rm $(IMAGE_NAME)
