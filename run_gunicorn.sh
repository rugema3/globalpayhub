#!/bin/bash
# This script starts a Gunicorn server in the background using nohup


APP_ENTRY_POINT="app1:app"

# Run Gunicorn with nohup to keep it running even if the terminal is closed
nohup gunicorn $APP_ENTRY_POINT &

# Print a message indicating that the Gunicorn server has been started
echo "Gunicorn server started in the background. PID: $!"
