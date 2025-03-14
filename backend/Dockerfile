FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create a sample .env file if it doesn't exist (for build purposes only)
RUN if [ ! -f .env ]; then \
    echo "SECRET_KEY=build_time_dummy_key" > .env; \
    echo "DEBUG=True" >> .env; \
    echo "ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0" >> .env; \
    echo "POSTGRES_USER=postgres" >> .env; \
    echo "POSTGRES_PASSWORD=postgres" >> .env; \
    echo "POSTGRES_DB=postgres" >> .env; \
    echo "POSTGRES_HOST=db" >> .env; \
    echo "POSTGRES_PORT=5432" >> .env; \
    echo "DATABASE_URL=postgres://\${POSTGRES_USER}:\${POSTGRES_PASSWORD}@\${POSTGRES_HOST}:\${POSTGRES_PORT}/\${POSTGRES_DB}" >> .env; \
    fi

# Run migrations and collect static files at build time (optional)
# RUN python manage.py migrate
# RUN python manage.py collectstatic --noinput

EXPOSE 8000


COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]