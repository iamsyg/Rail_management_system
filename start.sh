#!/bin/bash
set -e

echo "Fetching Prisma binaries..."
python -m prisma py fetch

echo "Starting application..."
python -m website.app.pages.api.user.server