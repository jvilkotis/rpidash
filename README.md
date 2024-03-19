# rpidash

Flask-based dashboard for headless Raspberry Pi system health monitoring.

![screenshot](rpidash/static/screenshot.png)

## Installation

### Docker compose

```YAML
version: "3.8"
services:
  rpidash:
    build: https://github.com/jvilkotis/rpidash.git
    ports:
      - 5000:5000
    volumes:
      - /path/to/data:/data
    environment:
      UID: 1000
      GID: 1000
      FLASK_ENV: production
```

The host directory `/path/to/data` is mounted to `/data` in the container, enabling persistent storage for the SQLite
database and application configuration.

## Development server

```Shell
python3 -m venv .venv
```

```Shell
. .venv/bin/activate
```

```Shell
pip install -r requirements.txt
```

```Shell
FLASK_ENV=development flask --app rpidash run --debug
```

## Testing

### Unit tests

```Shell
FLASK_ENV=testing python3 -m unittest discover
```

### Coverage

```Shell
FLASK_ENV=testing coverage run -m unittest discover
```

```Shell
coverage report
```

```Shell
coverage html
```