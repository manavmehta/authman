# Variables
POSTGRES_VERSION := 14.5-alpine
KEYCLOAK_SERVER_VERSION := latest
ECR_URI := 952057567027.dkr.ecr.ap-south-1.amazonaws.com

# Phony targets
.PHONY: build pull tag push

# Default target
all: build pull tag push

# Build services defined in your docker-compose file
build:
	@echo "Building the services defined in your docker-compose file"
	@docker buildx build --platform linux/amd64 -t auth_service_backend:latest . --load 
	@echo "Done!"


# Pull public images
pull:
	@echo "Pulling public images"
	@docker pull --platform linux/amd64 postgres:$(POSTGRES_VERSION)
	@docker pull --platform linux/amd64 nginx:alpine
	@docker pull --platform linux/amd64 bitnami/keycloak:$(KEYCLOAK_SERVER_VERSION)
	@echo "Done!"

# Tag images for ECR
tag:
	@echo "Tagging images for ECR"
	@docker tag postgres:$(POSTGRES_VERSION) $(ECR_URI)/postgres:$(POSTGRES_VERSION)
	@docker tag bitnami/keycloak:$(KEYCLOAK_SERVER_VERSION) $(ECR_URI)/keycloak:$(KEYCLOAK_SERVER_VERSION)
	@docker tag auth_service_backend:latest $(ECR_URI)/authman-backend:latest
	@docker tag nginx:alpine $(ECR_URI)/nginx:alpine
	@echo "Done!"

# Push images to ECR
push:
	@echo "Pushing images to ECR"
	@$(eval export AWS_PROFILE=default)
	@docker login -u AWS -p $$(aws ecr get-login-password --region ap-south-1 --profile hackathon --no-verify-ssl) $(ECR_URI)
	@docker push $(ECR_URI)/postgres:$(POSTGRES_VERSION)
	@docker push $(ECR_URI)/keycloak:$(KEYCLOAK_SERVER_VERSION)
	@docker push $(ECR_URI)/authman-backend:latest
	@docker push $(ECR_URI)/nginx:alpine
	@echo "Done!"