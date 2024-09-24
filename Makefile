env-file:
	@cp .env.example ./src/.env
start-keycloak-svc:
	@cd deployment && docker compose up -d keycloak
	@echo "IDP service: http://localhost:8080"
start-orders-svc:
	@cd deployment && docker compose --env-file ../src/.env up -d orders-service --build
	@echo "Order service: http://localhost:8000"
restart-keycloak-svc:
	@cd deployment && docker compose restart keycloak
restart-orders-svc:
	@cd deployment && docker compose restart orders-service
stop:
	@cd deployment && docker compose down
