
# Python Decorators Project

This directory contains examples and utilities demonstrating the use of Python decorators for database operations, logging, caching, and error handling.

## Contents

- `0-log_queries.py`: Decorator for logging SQL queries.
- `1-with_db_connection.py`: Decorator to manage database connections.
- `2-transactional.py`: Decorator for handling transactions.
- `3-retry_on_failure.py`: Decorator to retry failed operations.
- `4-cache_query.py`: Decorator to cache query results.
- `setup_db.py`: Script to set up the database.
- `users.db`: SQLite database file.
- `README.md`: Project documentation.

## Usage

1. Activate the virtual environment:
	```bash
	source env/bin/activate
	```
2. Run any script to see the decorator in action:
	```bash
	python python-decorators-0x01/0-log_queries.py
	```

## Requirements

- Python 3.12+
- SQLite3

## Description

Each script demonstrates a specific decorator pattern for database-related tasks. These decorators help improve code modularity, readability, and maintainability.
