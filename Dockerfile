# Dockerfile
FROM python:3.10 as base

# Set environment variables for Poetry
ENV POETRY_VERSION=1.8.4
ENV PATH="/root/.local/bin:$PATH"

# Install Poetry
RUN pip install --no-cache-dir poetry==$POETRY_VERSION

WORKDIR /app

# Copy only the necessary files for installing dependencies first
COPY pyproject.toml poetry.lock* /app/

# Copy the rest of the application code
COPY . /app

# ----------------------
# Test stage
# ----------------------
FROM base as test
# Install dev dependencies (includes pytest and other testing tools)
RUN poetry install --no-root

# Default command for the test stage
CMD ["poetry", "run", "pytest", "--cov=app", "--cov-report=term-missing", "--maxfail=1", "--disable-warnings", "-q"]


# ----------------------
# Final stage for production
# ----------------------
FROM base as production
# Install dependencies
RUN poetry install --no-root --no-dev

# Command to run the application
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]