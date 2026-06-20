[![Django CI](https://github.com/tonytech83/warranty_keeper/actions/workflows/django-ci.yml/badge.svg)](https://github.com/tonytech83/warranty_keeper/actions/workflows/django-ci.yml)

## WARRANTY KEEPER
Warranty Keeper is a Django web application for managing your warranties and suppliers.
Store purchase details, warranty periods, prices and supplier info, and keep an eye on
what's expiring from a single dashboard.

<div align="center" display="flex">
    <img src="./docs/pic-1.webp" alt="warranty keeper">
</div>

<br/>

### Features
- **Dashboard** with KPI cards (totals, active, expiring soon, expired, suppliers, total value),
  colour-coded "expiring soon" alerts, recently-added items, and charts (status, warranties per
  supplier, expirations over the next 12 months) powered by Chart.js.
- **Warranties** — create / view / edit / soft-delete, with item, purchase date, period, price,
  description, invoice image and supplier.
- **Suppliers** — create / view / edit / soft-delete, with logo, email, phone and website.
- **MariaDB** storage — runs in its own container, with data persisted in a named Docker volume.

### Configuration
Copy `.env.example` to `.env` and adjust as needed:

| Variable        | Default                       | Description                                   |
| --------------- | ----------------------------- | --------------------------------------------- |
| `SECRET_KEY`    | insecure dev key              | Django secret key — **set your own**.         |
| `DEBUG`         | `True`                        | Set to `False` when exposing the app.         |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1,[::1]`   | Comma-separated list of allowed hosts.        |
| `CURRENCY`      | `€`                           | Currency symbol shown next to prices.         |
| `DB_NAME`       | `warranty_keeper`             | Database name.                                |
| `DB_USER`       | `warranty`                    | Database user.                                |
| `DB_PASSWORD`   | —                             | Database user password — **set your own**.    |
| `DB_ROOT_PASSWORD` | —                          | MariaDB root password (container admin).       |
| `DB_HOST`       | `db` (Docker) / `127.0.0.1`   | Database host.                                |
| `DB_PORT`       | `3306`                        | Database port.                                |

### Run with Docker (recommended)
```bash
docker compose up --build
```
This starts two containers: `db` (MariaDB) and `web` (the Django app). The `web`
container waits for the database to become healthy, then runs migrations
automatically before serving. Open http://localhost:8181.

**Persistence**

- **Database** — stored in the `db_data` named Docker volume. It survives
  `docker compose down` and container rebuilds. To start completely fresh, remove
  the volume: `docker compose down -v`.
- **Uploaded media** (invoices & supplier logos) — bind-mounted to `./mediafiles`,
  overridable with `MEDIA_DIR` in `.env`. Point it at a NAS/share for easy backups.

To back up the database, use `mysqldump` against the `db` container, e.g.:
```bash
docker compose exec db sh -c \
  'mariadb-dump -u"$MARIADB_USER" -p"$MARIADB_PASSWORD" "$MARIADB_DATABASE"' > backup.sql
```

### Run locally
Running outside Docker requires a MariaDB/MySQL server. Create the database and
user, then set `DB_*` in `.env` (use `DB_HOST=127.0.0.1`):
```bash
python -m venv venv
# Windows: venv\Scripts\activate   |   Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

To use the Django admin, create a superuser: `python manage.py createsuperuser`.

<h6 align="center"> Made by Anton Petrov </h6>
