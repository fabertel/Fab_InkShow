
#!/bin/bash


# Define the working directory and Python virtual environment
WORKDIR="/root/TIG/Fab_InkShow"  # Change this to your actual project path
APP_SCRIPT="$WORKDIR/FAB_inkshow.py"
VENV="$WORKDIR/venv/bin/activate"
LOGFILE="$WORKDIR/FAB_inkshow.log"

# Define FastAPI App and Port
APP_MODULE="FAB_inkshow:app"
PORT=8000

# Check if the script is already running
if pgrep -f "uvicorn FAB_inkshow:app" > /dev/null; then
    echo "🚀 FAB_inkshow is already running on port $PORT!"
    exit 1
fi

echo "🔄 Starting FAB_inkshow FastAPI app..."
cd "$WORKDIR" || exit 1

# Activate virtual environment
source "$VENV"

# Run Uvicorn in the background and log output
nohup uvicorn "$APP_MODULE" --host 0.0.0.0 --port "$PORT" --reload > "$LOGFILE" 2>&1 &


echo "✅ FAB_inkshow started successfully! Logs: $LOGFILE"
