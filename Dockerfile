FROM python:3.11-slim

WORKDIR /app

# Copy both pyproject.toml and source
COPY pyproject.toml .
COPY src/ ./src
COPY tests/ ./tests

# Install core + dev dependencies
RUN pip install --no-cache-dir .

CMD ["python", "-m", "aws_costs.aws_cost_report"]
