# ─────────────────────────────────────────────────────
# Multi-stage Dockerfile for Python FastAPI Application
# ─────────────────────────────────────────────────────
# This Dockerfile uses multi-stage build to:
# 1. Reduce final image size (no build tools in production)
# 2. Improve security (non-root user, minimal dependencies)
# 3. Optimize build cache (requirements installed separately)
# ─────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────
# Stage 1: Builder
# ─────────────────────────────────────────────────────
# Install dependencies in isolated virtual environment
FROM python:3.12-slim AS builder

# Set working directory for all subsequent commands
WORKDIR /app

# Create virtual environment for isolated dependencies
# This keeps dependencies separate from system Python
RUN python -m venv .venv

# Add virtual environment to PATH
# All pip commands will use this venv
ENV PATH="/app/.venv/bin:$PATH"

# Copy requirements file first (Docker cache optimization)
# If requirements.txt doesn't change, this layer is cached
COPY src/requirements.txt .

# Install Python dependencies
# --no-cache-dir: Don't store pip cache (reduces image size)
RUN pip install --no-cache-dir -r requirements.txt


# ─────────────────────────────────────────────────────
# Stage 2: Runtime (Production)
# ─────────────────────────────────────────────────────
# Minimal production image with only what's needed to run
FROM python:3.12-slim AS runtime

# Set working directory for application files
WORKDIR /app

# Install curl for health checks (removed in final layer)
# --no-install-recommends: Don't install recommended packages (reduces size)
# rm -rf /var/lib/apt/lists/*: Clean up apt cache (reduces size)
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
# Running as root is a security risk (container escape vulnerability)
# chown /app: Give user ownership of working directory
RUN useradd -m appuser && chown appuser:appuser /app

# Switch to non-root user
# All subsequent commands and CMD run as appuser
USER appuser

# Copy virtual environment from builder stage
# --chown: Set correct ownership for appuser
# Only .venv is copied (no build tools, no source code yet)
COPY --from=builder --chown=appuser:appuser /app/.venv /app/.venv

# Copy application source code
# All files from build context are copied
# --chown: Set correct ownership for appuser
COPY --chown=appuser:appuser . .

# Add virtual environment to PATH (same as builder)
# Makes uvicorn, python, pip available without activation
ENV PATH="/app/.venv/bin:$PATH"

# Python runtime optimizations:
# PYTHONDONTWRITEBYTECODE=1: Don't create .pyc files (reduces I/O)
# PYTHONUNBUFFERED=1: Don't buffer stdout/stderr (logs appear immediately)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Expose application port
# This documents which port the app listens on
# Doesn't actually publish the port (use -p in docker run)
EXPOSE 8000

# Default command to run when container starts
# Uvicorn ASGI server with host 0.0.0.0 (accessible from outside)
# CMD can be overridden in docker-compose.yml or docker run
CMD [ "uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000" ]
