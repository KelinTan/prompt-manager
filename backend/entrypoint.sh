#!/bin/sh

set -e  # 出错立即退出

echo "🚀 Starting FastAPI web server..."
exec poetry run uvicorn src.main:app --host 0.0.0.0 --port 8080 --no-access-log