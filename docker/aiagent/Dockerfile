# syntax=docker/dockerfile:1.4
FROM python:3.10-alpine

# Set environment variables to avoid Python bytecode caching
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Add /aiagent to PYTHONPATH
ENV PYTHONPATH=/

# Set working directory
WORKDIR /aiagent

# Install system dependencies (e.g., PostgreSQL client for QuestDB)
RUN apk add --no-cache gcc g++ musl-dev libpq-dev postgresql-client

# Copy requirements file and install dependencies
COPY requirements.txt /aiagent
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /aiagent

# Expose the port the Flask app will run on
EXPOSE 5001

# Set the default entrypoint and command
ENTRYPOINT ["python3"]
CMD ["run.py"]
