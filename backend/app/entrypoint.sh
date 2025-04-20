#!/bin/bash

echo "Checking for database..."
python app/init_db.py
if [ $? -ne 0 ]; then
    echo "Database initialization failed! Exiting."
    exit 1
fi

echo "Starting Flask app..."
python run.py
