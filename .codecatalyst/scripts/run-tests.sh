#!/bin/bash

echo "Running unit tests..."
PYTHONPATH=WarhammerDiscordBot pytest --junitxml=test_results.xml --cov-report xml:test_coverage.xml --cov=. WarhammerDiscordBot/tests/unit/
