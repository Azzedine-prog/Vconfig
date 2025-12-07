# Vconfig

A lightweight vector configurator inspired by Eclipse-style tooling. Use the command-line interface to create, inspect, and normalize numeric vector configurations stored as JSON files.

## Getting started

Requires Python 3.10+ and `pip`.

```bash
pip install -r requirements.txt
```

## Usage

Initialize a new vector configuration (components default to `0.0`):

```bash
python -m src.vector_configurator init PositionVector 3 position.json
```

Update a single component:

```bash
python -m src.vector_configurator update position.json 1 2.5
```

Inspect the configuration and its magnitude:

```bash
python -m src.vector_configurator info position.json
```

Normalize the vector and write the result to a new file:

```bash
python -m src.vector_configurator normalize position.json position.normalized.json
```

## Development

Run the automated tests with `pytest`:

```bash
pytest
```
