help: ## Show help
	@echo "Usage: make [target]"
	@echo "Targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

weekly_pager: ## Add daily pager for the next 7 days
	pipenv run python run.py --dry-run pager --start-date $(shell date +%Y-%m-%d) --duration 7
