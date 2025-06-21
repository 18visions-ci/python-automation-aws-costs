FROM python:3.11-slim

# Set working dir
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script
COPY aws_cost_report.py .

# Default run command
CMD ["python", "aws_cost_report.py"]
