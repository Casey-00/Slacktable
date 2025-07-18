#!/usr/bin/env python3
"""
Simple runner script for Socket Mode.
Run this to test the app locally with Socket Mode.
"""

import asyncio
import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.socket_mode import run_socket_mode

if __name__ == "__main__":
    asyncio.run(run_socket_mode())
