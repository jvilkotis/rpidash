# rpidash

Flask-based dashboard for headless Raspberry Pi system health monitoring.

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