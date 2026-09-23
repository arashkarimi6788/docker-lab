# docker-lab

Exploratory Docker work for Month 4 — a Flask API backed by Postgres,
containerized and wired together with docker compose.

## What's here

| File | Purpose |
|---|---|
| `app.py` | Flask API with `POST /items` and `GET /items`, using `psycopg2` to talk to Postgres |
| `requirements.txt` | Python dependencies (Flask, psycopg2-binary) |
| `Dockerfile` | Builds the Flask app into its own image |
| `docker-compose.yml` | Wires the Flask app and a Postgres container together |
| `.env` (not committed) | Postgres credentials, read by compose |

## Concepts proven

- **Custom image**: `Dockerfile` builds the app into its own image rather
  than relying on someone else's. Layer ordering matters —
  `requirements.txt` is copied and installed before `app.py`, so Docker's
  build cache reuses the dependency-install layer when only the app code
  changes.
- **Multi-container orchestration**: `docker-compose.yml` defines two
  services (`web`, `db`) that start together as one unit.
- **Service-name networking**: Flask reaches Postgres using the hostname
  `db` — the literal name of the compose service — with no manual IP
  configuration. Compose creates the network and DNS resolution
  automatically.
- **Healthcheck-gated startup**: `depends_on: condition: service_healthy`
  ensures Flask only starts once Postgres is actually ready to accept
  connections (via `pg_isready`), not just once the container exists —
  avoiding a real, common startup-race bug.
- **Persistent storage**: a named volume (`pgdata`) holds Postgres's data.
  Verified by inserting rows via the API, running a full
  `docker compose down` (which removes the containers entirely) followed
  by `docker compose up`, and confirming the data was still present
  afterward.
- **Secrets out of code**: DB credentials are read from environment
  variables (`os.environ`) in `app.py`, sourced from a local `.env` file
  that is git-ignored — never hardcoded or committed.

## Verified end to end

Full round trip via curl: `POST /items` inserts a row, `GET /items`
returns it. Confirmed persistence survives a full container teardown and
recreation.
