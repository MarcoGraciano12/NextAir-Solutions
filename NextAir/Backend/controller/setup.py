"""
Logging system configuration module.

Configures application-wide logging with daily file rotation
and environment-based log level control.

Author: Marco Graciano
Date: March 03, 2026
"""

import os
import logging
from logging.handlers import TimedRotatingFileHandler

# Read log level from environment (default: INFO)
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()

# Read backup count from environment (default: 7)
BACKUP_COUNT = int(os.getenv('LOG_BACKUP_COUNT', '7'))

# Configure file handler with daily rotation
file_handler = TimedRotatingFileHandler(
    "/logs/system.log",
    when="midnight",
    interval=1,
    backupCount=BACKUP_COUNT,
    encoding="utf-8"
)

# Set log level for file handler
file_handler.setLevel(getattr(logging, LOG_LEVEL))

# Define log message format
file_formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s", "%Y-%m-%d %H:%M:%S")

# Apply formatter to file handler
file_handler.setFormatter(file_formatter)

# Set up basic logging configuration
logging.basicConfig(level=getattr(logging, LOG_LEVEL), handlers=[file_handler], force=True)
