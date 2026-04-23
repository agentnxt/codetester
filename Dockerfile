FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml README.md ./
COPY src/ ./src/
COPY examples/ ./examples/

# Install Python dependencies
RUN pip install --no-cache-dir -e ".[dev]"

# Set default command
CMD ["python", "-c", "print('CodeTester agent ready!')"]