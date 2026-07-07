# ==========================================================================
# BUSINESS OS - STANDARDIZED DOCKER RUNTIME (BRO'S ARCHITECTURE SPEC)
# ==========================================================================

# --- STAGE 1: DEPENDENCY BUILDER ENGINE ---
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    libssl-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt

# --- STAGE 2: FIXED HARDENED RUNTIME ---
FROM python:3.11-slim AS runtime

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=production

# Enforce explicit exposure contract
EXPOSE 8000

# Fixed Dynamic Port Runtime Engine matching Bro's instruction
CMD ["sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
