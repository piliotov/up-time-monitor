# Uptime Monitor

A website uptime monitoring tool that checks website availability at configurable intervals and stores historical data for analysis.

## Features

- Configurable URL monitoring with custom check intervals
- Tracks HTTP status codes and response latency
- Stores check results in SQLite database for retrospective analysis
- Configurable timeout and maximum acceptable latency thresholds
- Scheduling for continuous monitoring

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/piliotov/up-time-monitor.git
cd up-time-monitor
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate # Mac/Linux
# or
.venv\Scripts\activate  # Windows
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Edit the `config.json` file to configure the monitoring parameters:

```json
{
  "url": "https://example-site.com",
  "interval_sec": 60,
  "timeout_sec": 10,
  "max_latency_ms": 2000
}
```

### Configuration Parameters

- **url**: The website's URL to monitor
- **interval_sec**: Time interval between checks in sec
- **timeout_sec**: HTTP request timeout in sec
- **max_latency_ms**: Maximum acceptable response latency in ms

## Running the Application

Start the monitoring tool:

```bash
python main.py
```

The application will:
1. Perform an initial check immediately
2. Continue checking at the configured interval
3. Store all results in `uptime_monitor.db`

To stop the monitoring, press `Ctrl+C`.

## Data Storage

All check results are stored in a SQLite database (`uptime_monitor.db`) with the following schema:

- **id**: Unique check identifier
- **ts_utc**: Timestamp (UTC) of the check
- **status_code**: HTTP status code (or NULL if request failed)
- **ok_state**: 1 if check passed (status 2xx/3xx and latency within threshold), 0 otherwise
- **latency_ms**: Response time in milliseconds
- **error_msg**: Error message if the check failed