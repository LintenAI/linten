#!/bin/bash
# Parallel Linten Health Check Runner (Bash version)
#
# This script runs multiple health check containers in parallel.
#
# Usage:
#   export LINTEN_BASE_URL="https://linten.example.com"
#   export LINTEN_API_KEY="<your-virtual-key>"
#   ./run_parallel_health_checks.sh [num_parallel_jobs] [image_name] [container_runtime]
#
# Defaults:
#   - num_parallel_jobs: 16
#   - image_name: linten/linten-health-check:latest
#   - container_runtime: docker

set -e

# Default values
NUM_PARALLEL_JOBS="${1:-16}"
IMAGE_NAME="${2:-linten/linten-health-check:latest}"
CONTAINER_RUNTIME="${3:-docker}"

# Require credentials for the target proxy
if [ -z "$LINTEN_BASE_URL" ]; then
    export LINTEN_BASE_URL="https://linten-perf-cache-and-router.onrender.com"
    echo "Warning: LINTEN_BASE_URL not set, using default: $LINTEN_BASE_URL" >&2
fi

: "${LINTEN_API_KEY:?set LINTEN_API_KEY}"

# Check if container runtime is available
if ! command -v "$CONTAINER_RUNTIME" &> /dev/null; then
    echo "Error: $CONTAINER_RUNTIME is not installed" >&2
    exit 1
fi

# Print configuration
echo "Running $NUM_PARALLEL_JOBS parallel health check containers..."
echo "Using image: $IMAGE_NAME"
echo "Container runtime: $CONTAINER_RUNTIME"
echo "Linten Base URL: $LINTEN_BASE_URL"
echo ""
echo "NOTE: This will run continuously. Press Ctrl+C to stop."
echo ""
echo "Troubleshooting:"
echo "  - If you see 'All connection attempts failed', check:"
echo "    1. Is the Linten proxy running on the expected port?"
echo "    2. Set LINTEN_BASE_URL to the correct URL (e.g., http://host.docker.internal:PORT)"
echo "    3. On Linux, you may need to use the host IP instead of host.docker.internal"
echo ""

# Function to run a single health check container
run_health_check() {
    local env_vars=(
        -e "LINTEN_BASE_URL=$LINTEN_BASE_URL"
        -e "LINTEN_API_KEY=$LINTEN_API_KEY"
        -e "LINTEN_JSON_OUTPUT=true"
    )
    
    # Pass through custom auth header if set
    if [ -n "$LINTEN_CUSTOM_AUTH_HEADER" ]; then
        env_vars+=(-e "LINTEN_CUSTOM_AUTH_HEADER=$LINTEN_CUSTOM_AUTH_HEADER")
    fi
    
    "$CONTAINER_RUNTIME" run --rm "${env_vars[@]}" "$IMAGE_NAME"
}

# Run parallel health checks
# This creates an infinite loop that keeps spawning containers
# Each container tests all models, then exits, and a new one starts
while true; do
    # Start containers in parallel using background jobs
    pids=()
    for ((i=1; i<=NUM_PARALLEL_JOBS; i++)); do
        run_health_check &
        pids+=($!)
    done
    
    # Wait for all background jobs to complete
    for pid in "${pids[@]}"; do
        wait "$pid" 2>/dev/null || true
    done
done
