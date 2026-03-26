"""
Database package.

Author: Marco Graciano
Date: 2025-03-26

Exposes engine, Base, and database initialization function.
"""

from .engine import engine, Base, init_db

__all__ = ["engine", "Base", "init_db"]
