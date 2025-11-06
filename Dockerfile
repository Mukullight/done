FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy poetry.toml (and poetry.lock if available)
COPY poetry.toml ./

# Install dependencies without creating a virtualenv (for Docker)
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of the application code
COPY . .

# Expose the port (assuming the app runs on 8050 for Dash, adjust if needed)
EXPOSE 8050

# Command to run the application
CMD ["python", "-m", "dashboard.main"]