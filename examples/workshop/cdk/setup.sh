#!/bin/bash

# Exit on any error, undefined variable, or pipe failure
set -euo pipefail

error_handler() {
    echo "Error occurred in script at line: ${1}"
    exit 1
}

trap 'error_handler ${LINENO}' ERR

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# Check if CDK is installed
if ! command -v cdk &> /dev/null; then
    log "CDK is not installed. Please install it first."
    exit 1
fi

main() {
    log "Starting workshop setup"

    # Create and activate python virtual environment called .venv
    log "Creating virtual environment"
    python3 -m venv .venv
    source .venv/bin/activate
    log "Virtual environment created and activated"
    
    # Install dependencies
    log "Installing dependencies"
    pip install -r requirements.txt
    log "Dependencies installed"

    # Run CDK build
    log "Bootstrapping CDK"
    cdk bootstrap
    log "CDK bootstrapped"
    log "Running CDK deploy"
    cdk deploy --require-approval never
    log "CDK deployed"
}

# Run the main function
main
