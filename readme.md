# AWS Cost Reporter

Fetches AWS daily and month-to-date (MTD) costs and posts summaries to Discord.

## Features

- Retrieves AWS cost data using the Cost Explorer API.
- Summarizes daily costs by service and usage type.
- Summarizes month-to-date costs.
- Posts a summary to a Discord channel via webhook.
- Can be run locally, in Docker, or via CI/CD (e.g., Jenkins).

## Requirements

- Python 3.8+
- AWS credentials with Cost Explorer access
- Discord webhook URL

## Installation

Install with pip (editable mode recommended for development):

```sh
pip install -e .
```

Or use Docker (recommended for CI/CD):
```sh
docker build -t aws-cost-reporter .
```
## Usage
Locally
Set the required environment variables:

DISCORD_WEBHOOK_URL
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_DEFAULT_REGION (e.g., us-west-2)

Then run:
```sh
python -m aws_costs.aws_cost_report
```

## With Docker
```sh
docker run --rm \
  -e DISCORD_WEBHOOK_URL=your_webhook_url \
  -e AWS_ACCESS_KEY_ID=your_access_key \
  -e AWS_SECRET_ACCESS_KEY=your_secret_key \
  -e AWS_DEFAULT_REGION=us-west-2 \
  aws-cost-reporter
```

## With Jenkins
This repository includes two Jenkinsfiles for CI/CD:

### `Jenkinsfile` (Scheduled Cost Reporting)
This pipeline runs the cost reporter on a schedule (e.g., daily). It uses Jenkins credentials to securely store the `DISCORD_WEBHOOK_URL` and AWS credentials.

### `Jenkinsfile_build` (Docker Image Build)
This pipeline automates building and publishing the application's Docker image.
- It builds the Docker image.
- It tags the image with the build number and `latest`.
- It pushes the image to a container registry.
- It sends build status notifications (success or failure) to a Discord channel.

This pipeline requires a 'Secret text' credential with the ID `discord-webhook-url` for the Discord webhook.

## Configuration
Edit pyproject.toml to manage dependencies.
The main logic is in src/aws_costs/aws_cost_report.py.

## Testing
Run tests with:
```sh
pytest
```

