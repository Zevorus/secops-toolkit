# Google SecOps & Threat Intel Automation Toolkit

A clean, modular Python-based CLI/Library for interacting with Google Security Operations (Chronicle) and Google Threat Intelligence (GTI) via their RESTful APIs.

## Project Structure

```text
secops-toolkit/
├── pyproject.toml           # Project metadata and dependencies
├── README.md                # Documentation
├── .env                     # Environment variables (API endpoints, credentials)
├── .gitignore               # Ignored files (venv, .env, __pycache__)
├── src/
│   └── secops_toolkit/      # Main package
│       ├── __init__.py      # Package initialization
│       ├── cli.py           # CLI Entrypoint (Click-based)
│       ├── clients/         # Client implementations
│       │   ├── __init__.py
│       │   ├── secops_client.py
│       │   └── threat_intel_client.py
│       └── utils/           # Utility functions (auth, etc.)
│           ├── __init__.py
│           └── auth.py
└── tests/                   # Unit and integration tests
    ├── __init__.py
    └── test_clients.py
```

## Features

- **Google SecOps Client**: Manage rules, list instances, and test connectivity.
- **Google Threat Intelligence Client**: Access GTI findings and alerts.
- **CLI Interface**: Perform common tasks directly from the terminal.
- **Modular Design**: Clients can be easily used as a library in other projects.

## Setup

1.  **Requirement**: Ensure you have Python 3.10+ installed.
2.  **Environment Variables**: Create a `.env` file with the following variables:
    ```env
    API_ENDPOINT=https://backstory.googleapis.com
    SECOPS_PROJECT_NUMBER=123456789
    SECOPS_INSTANCE_ID=00000000-0000-0000-0000-000000000000
    SECOPS_LOCATION=us
    ```
3.  **Install Application**:
    ```bash
    pip install -e .
    ```

## Usage

### CLI
```bash
# Test SecOps connectivity
secops-toolkit secops test-connectivity

# List SecOps rules
secops-toolkit secops list-rules --page-size 5

# List GTI alerts
secops-toolkit gti list-alerts
```

### Library
```python
from secops_toolkit.clients import SecOpsClient

client = SecOpsClient()
rules = client.list_rules()
```
