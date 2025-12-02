#!/bin/bash
# Cutoff Time API - Demo Launcher for Linux/Mac

echo ""
echo "===================================="
echo "  Cutoff Time API - Demo Launcher"
echo "===================================="
echo ""

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "[ERROR] Poetry is not installed!"
    echo "Please install Poetry first: https://python-poetry.org/docs/#installation"
    exit 1
fi

echo "[1/3] Installing dependencies..."
poetry install

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies!"
    exit 1
fi

echo ""
echo "[2/3] Starting Cutoff Time API..."
echo ""
echo "===================================="
echo "  Demo Dashboard:"
echo "  http://localhost:8080/static/demo.html"
echo ""
echo "  API Documentation:"
echo "  http://localhost:8080/api/v1/docs"
echo "===================================="
echo ""
echo "[3/3] Server starting (press Ctrl+C to stop)..."
echo ""

poetry run uvicorn app.main:app --reload --port 8080
