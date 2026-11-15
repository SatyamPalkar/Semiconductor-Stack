# Local operation and later deployment

Use the exact setup/verification commands in README and Makefile. `make preview` serves `apps/web/out` independently of the API. With the API off, pages and charts still render from the database export; free-form questions show an honest offline state and recorded examples are clearly labelled.

The verified native database owns `data/native-postgres` on loopback/socket port 55432. The user's existing service on 5432 is untouched. `make native-up` checks the selected PostgreSQL/pgvector installation; `make native-down` stops only this cluster. Docker Compose is the portable recommended path but was not executed on this Mac because Docker is absent. Do not run native and Docker databases on 55432 simultaneously.

No cloud services or Terraform resources were created. AWS deployment requires a separate explicit user request and a current regional cost calculation. The future permanent showcase is a separate S3/CloudFront OAC stack with no API dependency. The temporary demo will use private RDS/pgvector, short API operations, on-demand ingestion/research tasks and bounded queues/status records. Code/docs for these are a later milestone; their mention here is not a deployment claim.

Before any public API deployment: add authentication or restricted demo access, bounded request bodies/rates, durable usage/model-cost limits, controlled jobs/checkpoints/retries, safe logs, secret storage, image scanning, smoke tests and rollback. CORS alone is not access control. Never expose local PostgreSQL or the development API to the internet.

## Local stop / rollback

Stop foreground preview/API with Ctrl+C. Use `make native-down` or `make db-stop` for the active database profile. Preserve `data/raw` originals, fixture metadata and database exports. Alembic revision 0003 deliberately refuses to restore NOT NULL period starts if those dates remain unknown; inventing financial metadata is not an acceptable rollback. Take a backup and create a fresh isolated database if a destructive schema reset is needed; never reset another project.

## Retained expansion preview (15 November 2026)

The local review remains available at `http://127.0.0.1:3100/value-chain/`, `/sources/` and `/industry-economics/`, with API docs at `http://127.0.0.1:8100/docs`. Stop only these known task-owned processes with `kill 54834` (static preview) and `kill 65736` (API), or Ctrl+C in their terminals. Restart with `make preview` and `make api`. See [the expansion report](industry-expansion-report.md) for actual verification and source scope. No hosted deployment was performed.
