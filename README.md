# Tiba HMIS

Tiba HMIS is a Flask-based hospital management dashboard. The app provides a dashboard shell with patient management, visit management, and AI assistance pages.

## What’s in the app

- Dashboard landing page
- Patient management pages
- Visit queue and visit entry pages
- AI help pages for patient overview, image analysis, and treatment planning

## Main routes

- `/` - dashboard home
- `/patients/` - patient list
- `/patients/new` - new patient form
- `/patients/triage` - triage page
- `/patients/sick-leave` - sick leave page
- `/patients/death-register` - death register page
- `/visits/` - visit queue
- `/visits/list` - visit list
- `/visits/new` - new visit page
- `/ai_help/` - AI patient overview
- `/ai_help/image-analysis` - AI image analysis
- `/ai_help/treatment-plan` - AI treatment plan

## Project structure

```text
app.py            # Flask entrypoint and app setup
routes/           # Blueprint modules for patients, visits, and AI help
templates/        # HTML templates
static/           # CSS, JS, images, and vendor assets
docker-compose.yml
Dockerfile
requirements.txt
```

## Requirements

- Python 3.13+
- Flask dependencies from `requirements.txt`
- A `SECRET_KEY` environment variable

## Local setup

1. Create and activate a virtual environment.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Create a local `.env` file.

```env
SECRET_KEY=your-secret-key
IS_DEBUG=True
PORT=5000
```

3. Run the app.

```bash
export FLASK_APP=app.py
flask run
```

4. Open the app in your browser.

```text
http://localhost:5000
```

## Docker setup

Docker Compose starts the Flask server in debug mode, which enables auto-reload when source files change.

The compose file uses collision-safe host ports by default:

- Web app: `http://localhost:5055`
- Postgres: `localhost:5433`

Start the stack with:

```bash
docker compose up --build
```

No separate server command is required after the containers start.

You can override the published ports with these environment variables:

- `WEB_HOST_PORT`
- `DB_HOST_PORT`

## Notes

- The UI branding currently says “Tiba HMIS”.
- Some templates still contain placeholder dashboard content and copied admin-theme text.
- The current `app.py` only requires `SECRET_KEY`; database and external service integrations are not wired in there yet.

## License

MIT. See [LICENSE](LICENSE).