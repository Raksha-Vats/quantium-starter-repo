#!/bin/bash

# Exit on any error
set -e

# Activate virtual environment
source venv/Scripts/activate

# Run pytest
pytest tests/

# Capture the exit code
exit_code=$?

# Exit with 0 if tests passed, 1 if they failed
if [ $exit_code -eq 0 ]; then
    echo "✅ All tests passed!"
    exit 0
else
    echo "❌ Some tests failed."
    exit 1
fi
