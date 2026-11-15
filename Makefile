export UV_CACHE_DIR := $(CURDIR)/.cache/uv
export UV_PYTHON_INSTALL_DIR := $(CURDIR)/.python

.PHONY: setup db-up migrate model ingest ingest-live api web test integration lint build evaluate snapshot verify db-stop
setup:
	uv sync --locked
	cd apps/web && npm ci
db-up:
	docker compose up -d --wait db
migrate:
	uv run alembic upgrade head
model:
	uv run semi prepare-model
ingest:
	uv run semi ingest --recorded
ingest-expanded:
	uv run semi ingest-expanded --recorded
ingest-expanded-live:
	uv run semi ingest-expanded
ingest-tsmc:
	uv run semi ingest-tsmc --recorded
ingest-tsmc-live:
	uv run semi ingest-tsmc
ingest-live:
	uv run semi ingest
api:
	uv run uvicorn apps.api.main:app --host 127.0.0.1 --port 8100 --no-access-log
web:
	cd apps/web && npm run dev
test:
	uv run pytest tests/unit -q
integration:
	RUN_DB_TESTS=1 uv run pytest tests/integration -q
lint:
	uv run ruff check .
	uv run ruff format --check .
	cd apps/web && npm run typecheck
build:
	cd apps/web && npm run build
evaluate:
	uv run semi evaluate
snapshot:
	uv run semi export-showcase
verify: lint test integration evaluate snapshot build
db-stop:
	docker compose stop db

native-up:
	bash scripts/native_postgres.sh
native-down:
	bash scripts/native_postgres.sh stop

e2e:
	cd apps/web && npm run test:e2e
preview:
	uv run python -m http.server 3100 --bind 127.0.0.1 --directory apps/web/out

.PHONY: native-up native-down preview e2e
