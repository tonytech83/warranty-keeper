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
- **SQLite** storage — zero-config, file-based, easy to back up (just copy the `.db` file).

### Configuration
Copy `.env.example` to `.env` and adjust as needed:

| Variable        | Default                       | Description                                   |
| --------------- | ----------------------------- | --------------------------------------------- |
| `SECRET_KEY`    | insecure dev key              | Django secret key — **set your own**.         |
| `DEBUG`         | `True`                        | Set to `False` when exposing the app.         |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1,[::1]`   | Comma-separated list of allowed hosts.        |
| `CURRENCY`      | `€`                           | Currency symbol shown next to prices.         |
| `SQLITE_PATH`   | `./db.sqlite3`                | Path to the SQLite database file.             |

### Run with Docker (recommended)
```bash
docker compose up --build
```
Then open http://localhost:8000. Migrations run automatically on startup.

**Persistence (bind mounts → real host files)**

The database and uploaded media are bind-mounted to host folders, so backups are
just file copies. The host paths default to `./data` and `./mediafiles`, and can be
overridden with `DATA_DIR` / `MEDIA_DIR` in `.env` file:

```
./data/db.sqlite3   # your database  (or $DATA_DIR/db.sqlite3)
./mediafiles/       # invoices & supplier logos  (or $MEDIA_DIR)
```

They survive `docker compose down` and `docker rm`, so a killed or rebuilt
container reopens the same database. To back up, copy `db.sqlite3`. To start fresh,
stop the app and delete it.

#### Storing the DB on a NAS / SMB share

You can point `DATA_DIR` at a network share for easy backups — **but SQLite needs POSIX byte-range locks, which SMB/CIFS does not provide.** For this reason disable SQLite file locking so the DB works on SMB/CIFS/NFS shares,which don't support POSIX locks. Safe with a single Gunicorn worker. If DB lives on a normal local filesystem, open `docker-compose.yml` and set to 0.
```
- SQLITE_NOLOCK=${SQLITE_NOLOCK:-1}
```

### Run locally
```bash
python -m venv venv
# Windows: venv\Scripts\activate   |   Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

To use the Django admin, create a superuser: `python manage.py createsuperuser`.

<h6 align="center"> Made by Anton Petrov </h6>
