# https://earthly.dev/blog/docker-and-makefiles/
DOCKER_USERNAME ?= daniloqueiroz
APPLICATION_NAME ?= beaver-base-env

build:
	docker build --network=host --tag ${DOCKER_USERNAME}/${APPLICATION_NAME} .
push:
	docker push ${DOCKER_USERNAME}/${APPLICATION_NAME}
run:
	docker run \
		--rm \
		--name beaver-base-env-test \
		--hostname beaver-base-env-test \
		-e TS_AUTH_KEY=tskey-auth-kC1VRF2CNTRL-RdaSXGoKf75kNJMq8WjB75tWcdtL7eLdh \
		daniloqueiroz/beaver:latest
exec:
	docker exec -it beaver-test /bin/fish
