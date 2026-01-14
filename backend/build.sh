#!/bin/bash
# Build and seed script for Render

# Install dependencies
pip install -r requirements.txt

# Run database seeding
python seed_data.py
