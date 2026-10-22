# Build stage & production image
FROM python:3.12-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    PORT=10000

# Set working directory
WORKDIR /app

# Install minimal OS dependencies for network health checks and PostgreSQL client libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first for layer caching
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application codebase
COPY . /app/

# Normalize line endings and execution permissions on entrypoint script
RUN sed -i 's/\r$//' /app/docker-entrypoint.sh \
    && chmod +x /app/docker-entrypoint.sh

# Create non-root system user and prepare writable instance directory
RUN groupadd -r appuser && useradd -r -g appuser appuser \
    && mkdir -p /app/instance /app/instance/downloads \
    && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Render assigns port dynamically via $PORT (defaults to 10000)
EXPOSE 10000

# Container healthcheck for Render zero-downtime deployment verification
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:${PORT:-10000}/api/health || exit 1

# Launch production server via entrypoint script
ENTRYPOINT ["/app/docker-entrypoint.sh"]
