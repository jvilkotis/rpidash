#!/bin/bash

SOURCE_CONFIG="/rpidash/rpidash/config.prod.yaml"
DEST_CONFIG="/data/config.yaml"

if [ ! -f "$DEST_CONFIG" ]; then
    cp "$SOURCE_CONFIG" "$DEST_CONFIG"
else
    echo "Config file already exists. Skipping copy operation."
fi

exec gunicorn -w 2 -b 0.0.0.0:5000 "rpidash:create_app()"