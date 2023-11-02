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
	@docker-compose build
	@echo "Done!"

# Pull public images
pull:
	@echo "Pulling public images"
	@docker pull postgres:$(POSTGRES_VERSION)
	@docker pull bitnami/keycloak:$(KEYCLOAK_SERVER_VERSION)
	@echo "Done!"

# Tag images for ECR
tag:
	@echo "Tagging images for ECR"
	@docker tag postgres:$(POSTGRES_VERSION) $(ECR_URI)/postgres:$(POSTGRES_VERSION)
	@docker tag bitnami/keycloak:$(KEYCLOAK_SERVER_VERSION) $(ECR_URI)/keycloak:$(KEYCLOAK_SERVER_VERSION)
	@docker tag auth_service_backend:latest $(ECR_URI)/authman-backend:latest
	@echo "Done!"

# Push images to ECR
push:
	@echo "Pushing images to ECR"
	@$(eval export AWS_PROFILE=default)
	@aws ecr get-login-password --profile treasure --region ap-south-1 --no-verify-ssl | docker login --username AWS --password-stdin $(ECR_URI)
	@docker push $(ECR_URI)/postgres:$(POSTGRES_VERSION)
	@docker push $(ECR_URI)/keycloak:$(KEYCLOAK_SERVER_VERSION)
	@docker push $(ECR_URI)/authman-backend:latest
	@echo "Done!"