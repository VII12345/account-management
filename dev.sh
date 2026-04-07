#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRONTEND_DIR="$ROOT_DIR/frontend"
BACKEND_DIR="$ROOT_DIR/backend"
AUTOSTRA_DIR="$ROOT_DIR/autostra"
AUTOSTRA_BACKEND_DIR="$AUTOSTRA_DIR/backend"
AUTOSTRA_FRONTEND_DIR="$AUTOSTRA_DIR/frontend"

VENV_DIR="${VENV_DIR:-$ROOT_DIR/.venv}"
if [[ -f "$VENV_DIR/bin/activate" ]]; then
  # shellcheck disable=SC1091
  source "$VENV_DIR/bin/activate"
else
  echo "Error: virtual environment not found at $VENV_DIR. Create it first." >&2
  exit 1
fi

PYTHON_BIN="${PYTHON_BIN:-$VENV_DIR/bin/python}"
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "Error: python not found in venv. Check $VENV_DIR or set PYTHON_BIN." >&2
  exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
  echo "Error: npm not found in PATH. Install Node.js or update PATH." >&2
  exit 1
fi

BACKEND_HOST="${BACKEND_HOST:-0.0.0.0}"
BACKEND_PORT="${BACKEND_PORT:-8080}"
FRONTEND_HOST="${FRONTEND_HOST:-0.0.0.0}"
START_AUTOSTRA_BACKEND="${START_AUTOSTRA_BACKEND:-1}"
START_AUTOSTRA_FRONTEND="${START_AUTOSTRA_FRONTEND:-1}"
AUTOSTRA_BACKEND_HOST="${AUTOSTRA_BACKEND_HOST:-0.0.0.0}"
AUTOSTRA_FRONTEND_HOST="${AUTOSTRA_FRONTEND_HOST:-0.0.0.0}"

cleanup() {
  if [[ -n "${BACKEND_PID:-}" ]] && kill -0 "$BACKEND_PID" 2>/dev/null; then
    kill "$BACKEND_PID" 2>/dev/null || true
  fi
  if [[ -n "${FRONTEND_PID:-}" ]] && kill -0 "$FRONTEND_PID" 2>/dev/null; then
    kill "$FRONTEND_PID" 2>/dev/null || true
  fi
  if [[ -n "${AUTOSTRA_BACKEND_PID:-}" ]] && kill -0 "$AUTOSTRA_BACKEND_PID" 2>/dev/null; then
    kill "$AUTOSTRA_BACKEND_PID" 2>/dev/null || true
  fi
  if [[ -n "${AUTOSTRA_FRONTEND_PID:-}" ]] && kill -0 "$AUTOSTRA_FRONTEND_PID" 2>/dev/null; then
    kill "$AUTOSTRA_FRONTEND_PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT INT TERM

# echo "Starting backend on http://${BACKEND_HOST}:${BACKEND_PORT}"
# (
#   cd "$BACKEND_DIR"
#   exec "$PYTHON_BIN" -m uvicorn main:app --reload --host "$BACKEND_HOST" --port "$BACKEND_PORT"
# ) &
# BACKEND_PID=$!

echo "Starting frontend on http://${FRONTEND_HOST}"
(
  cd "$FRONTEND_DIR"
  exec npm run dev -- --host "$FRONTEND_HOST"
) &
FRONTEND_PID=$!

if [[ "$START_AUTOSTRA_BACKEND" == "1" ]]; then
  if [[ -d "$AUTOSTRA_BACKEND_DIR" ]]; then
    echo "Starting autostra backend on http://${AUTOSTRA_BACKEND_HOST}"
    (
      cd "$AUTOSTRA_BACKEND_DIR"
      exec "$PYTHON_BIN" -m uvicorn main:app --reload --host "$AUTOSTRA_BACKEND_HOST"
    ) &
    AUTOSTRA_BACKEND_PID=$!
  else
    echo "Warning: autostra backend not found at $AUTOSTRA_BACKEND_DIR"
  fi
fi

if [[ "$START_AUTOSTRA_FRONTEND" == "1" ]]; then
  if [[ -d "$AUTOSTRA_FRONTEND_DIR" ]]; then
    echo "Starting autostra frontend on http://${AUTOSTRA_FRONTEND_HOST}"
    (
      cd "$AUTOSTRA_FRONTEND_DIR"
      exec npm run dev -- --host "$AUTOSTRA_FRONTEND_HOST"
    ) &
    AUTOSTRA_FRONTEND_PID=$!
  else
    echo "Warning: autostra frontend not found at $AUTOSTRA_FRONTEND_DIR"
  fi
fi

if wait -n 2>/dev/null; then
  wait -n
  exit_code=$?
else
  wait "$BACKEND_PID"
  exit_code=$?
fi

exit "$exit_code"
