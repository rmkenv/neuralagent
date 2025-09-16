# Multi-stage Dockerfile for Cognitive AI Clone Platform

# Base Python image with ML libraries
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Development stage
FROM base as development

WORKDIR /app

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Create necessary directories
RUN mkdir -p data/{assessments,profiles,training_data,models,chroma,ollama,logs} \
    && mkdir -p src/{cognitive_assessment,cognitive_profiling,llm_integration,memory_systems,web_interface} \
    && mkdir -p config tests scripts

# Copy application code
COPY . .

# Set permissions
RUN chmod +x scripts/*.sh 2>/dev/null || true

# Expose ports
EXPOSE 8501 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Default command
CMD ["streamlit", "run", "src/web_interface/streamlit_app.py", "--server.address", "0.0.0.0", "--server.port", "8501"]

# Production stage
FROM base as production

WORKDIR /app

# Copy only necessary files for production
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && python -m spacy download en_core_web_sm \
    && pip install gunicorn

# Copy application code (excluding development files)
COPY src/ ./src/
COPY config/ ./config/
COPY scripts/ ./scripts/
COPY .env.example .env

# Create non-root user for security
RUN groupadd -r cognitive && useradd -r -g cognitive cognitive \
    && mkdir -p data/{assessments,profiles,training_data,models,logs} \
    && chown -R cognitive:cognitive /app

# Switch to non-root user
USER cognitive

# Expose ports
EXPOSE 8501 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Production command with gunicorn
CMD ["streamlit", "run", "src/web_interface/streamlit_app.py", "--server.address", "0.0.0.0", "--server.port", "8501", "--server.headless", "true"]