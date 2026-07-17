# 1. USE LIGHTWEIGHT LINUX KERNEL BASE IMAGE WITH PYTHON 3.11 PRE-INSTALLED
FROM python:3.11-slim

# Enforce strict system-level environment runtime parameters tightly
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# 2. CREATE ISOLATED PRODUCTION ROOT WORKSPACE DIRECTORY
WORKDIR /app

# Install bare-essential security compilation dependencies natively
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 3. INGEST DEPENDENCIES PIPELINE ARRAYS SECURELY
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 4. COPY COMPREHENSIVE PRODUCTION PLATFORM SOURCE SHARDS
COPY . .

# Expose local ingress target mapping nodes
EXPOSE 8000

# 5. HARDENED BOOTSTRAP KERNEL COMMAND (RUNNING VIA UVICORN INDUSTRIAL ROUTERS)
CMD ["sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
