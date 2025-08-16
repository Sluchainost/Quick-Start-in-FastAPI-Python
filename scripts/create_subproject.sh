#!/bin/bash

# Usage: ./create_subproject.sh my_new_task

set -e

if [ -z "$1" ]; then
  echo "Usage: $0 <project_name>"
  exit 1
fi

PROJECT_NAME="$1"
PROJECT_ROOT="$PROJECT_NAME"

if [ -d "$PROJECT_ROOT" ]; then
  echo "Directory '$PROJECT_ROOT' already exists. Aborting to prevent overwrite."
  exit 2
fi

echo "Creating directory structure for '$PROJECT_ROOT'..."

# Create directories
mkdir -p "$PROJECT_ROOT/app/api/endpoints"
mkdir -p "$PROJECT_ROOT/app/api/schemas"
mkdir -p "$PROJECT_ROOT/app/core"
mkdir -p "$PROJECT_ROOT/app/db"
mkdir -p "$PROJECT_ROOT/app/exceptions"
mkdir -p "$PROJECT_ROOT/app/i18n/en/LC_MESSAGES"
mkdir -p "$PROJECT_ROOT/app/i18n/ru/LC_MESSAGES"
mkdir -p "$PROJECT_ROOT/app/repositories"
mkdir -p "$PROJECT_ROOT/app/services"
mkdir -p "$PROJECT_ROOT/app/utils"
mkdir -p "$PROJECT_ROOT/tests"

echo "Creating __init__.py and other base files..."

# App files
touch "$PROJECT_NAME"/app/__init__.py
touch "$PROJECT_NAME"/app/main.py

touch "$PROJECT_NAME"/app/api/__init__.py
touch "$PROJECT_NAME"/app/api/endpoints/__init__.py
touch "$PROJECT_NAME"/app/api/schemas/__init__.py

touch "$PROJECT_NAME"/app/core/__init__.py
touch "$PROJECT_NAME"/app/db/__init__.py
touch "$PROJECT_NAME"/app/exceptions/__init__.py
touch "$PROJECT_NAME"/app/repositories/__init__.py
touch "$PROJECT_NAME"/app/services/__init__.py
touch "$PROJECT_NAME"/app/utils/__init__.py

# i18n placeholders
touch "$PROJECT_NAME"/app/i18n/en/LC_MESSAGES/messages.po
touch "$PROJECT_NAME"/app/i18n/ru/LC_MESSAGES/messages.po
touch "$PROJECT_NAME"/app/i18n/README.md

# Tests
touch "$PROJECT_NAME"/tests/__init__.py
touch "$PROJECT_NAME"/tests/conftest.py
touch "$PROJECT_NAME"/tests/test_main.py

# Root files
touch "$PROJECT_NAME"/.env
touch "$PROJECT_NAME"/.env.example
touch "$PROJECT_NAME"/README.md

echo "Subproject '$PROJECT_NAME' scaffold created successfully!"
