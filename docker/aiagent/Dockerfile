FROM python:3.13.2-slim

# Set environment variables to avoid Python bytecode caching
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Add /aiagent to PYTHONPATH
ENV PYTHONPATH=/

# Set working directory
WORKDIR /aiagent

# Install system dependencies (e.g., PostgreSQL client for QuestDB)
RUN apt-get update && apt-get install -y \
    gcc g++ libpq-dev postgresql-client \
    && rm -rf /var/lib/apt/lists/*

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
