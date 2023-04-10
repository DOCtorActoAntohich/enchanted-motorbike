.PHONY: format
format:
	black ./enchanted_motorbike/ && ruff --fix ./enchanted_motorbike/

.PHONY: lint
lint:
	black --check ./enchanted_motorbike/ && \
		ruff ./enchanted_motorbike/ && \
		mypy --install-types --non-interactive ./enchanted_motorbike/
