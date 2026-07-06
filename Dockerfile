FROM python:3.13-slim

# Create non-root user for security
RUN addgroup --system app && adduser --system --group app

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends     libpq-dev     gcc     && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set permissions
RUN chown -R app:app /app
USER app

# Correct entrypoint path based on apps folder structure
CMD ["python", "-m", "uvicorn", "apps.main:app", "--host", "0.0.0.0", "--port", "8000"]
