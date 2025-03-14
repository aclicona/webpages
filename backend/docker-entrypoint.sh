#!/bin/bash
set -e

# Create the DATABASE_URL from individual parts
export DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"

# Execute the passed command
exec "$@"