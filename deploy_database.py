#!/usr/bin/env python3
"""
Database deployment script for Azure DevOps CI/CD pipeline.
This script handles database migrations and verification.
"""
import os
import sys
import logging
import subprocess
import argparse
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def check_environment():
    """Check that all required environment variables are set."""
    required_vars = [
        "POSTGRES_HOST",
        "POSTGRES_DB",
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
        "POSTGRES_PORT",
    ]

    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        logger.error(f"Missing required environment variables: {missing_vars}")
        return False

    logger.info("All required environment variables are set")
    return True


def install_dependencies():
    """Install required Python packages."""
    logger.info("Installing required dependencies...")

    try:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "sqlalchemy>=2.0.43",
                "alembic>=1.16.0",
                "psycopg2-binary>=2.9.0",
                "pydantic>=2.11.7",
                "pydantic-settings>=2.5.0",
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        logger.info("Dependencies installed successfully")
        return True

    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install dependencies: {e}")
        logger.error(f"STDOUT: {e.stdout}")
        logger.error(f"STDERR: {e.stderr}")
        return False


def run_alembic_command(command_args, cwd=None):
    """Run an alembic command and return the result."""
    try:
        cmd = [sys.executable, "-m", "alembic"] + command_args
        logger.info(f"Running: {' '.join(cmd)}")

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=cwd or Path(__file__).parent.parent,
            check=True,
        )

        if result.stdout:
            logger.info(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            logger.warning(f"STDERR:\n{result.stderr}")

        return True, result.stdout, result.stderr

    except subprocess.CalledProcessError as e:
        logger.error(f"Alembic command failed with exit code {e.returncode}")
        if e.stdout:
            logger.error(f"STDOUT:\n{e.stdout}")
        if e.stderr:
            logger.error(f"STDERR:\n{e.stderr}")
        return False, e.stdout or "", e.stderr or ""


def check_migration_status():
    """Check current migration status."""
    logger.info("Checking current migration status...")
    success, stdout, stderr = run_alembic_command(["current"])

    if success:
        logger.info("Migration status check completed")
        return True
    else:
        logger.error("Failed to check migration status")
        return False


def run_migrations():
    """Run database migrations."""
    logger.info("Running database migrations...")
    success, stdout, stderr = run_alembic_command(["upgrade", "head"])

    if success:
        logger.info("Database migrations completed successfully")
        return True
    else:
        logger.error("Database migrations failed")
        return False


def run_health_check():
    """Run comprehensive database health check."""
    logger.info("Running database health check...")

    try:
        script_path = Path(__file__).parent / "database_health_check.py"
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            check=True,
        )

        logger.info("Database health check completed successfully")
        logger.info(result.stdout)
        return True

    except subprocess.CalledProcessError as e:
        logger.error("Database health check failed")
        logger.error(f"STDOUT: {e.stdout}")
        logger.error(f"STDERR: {e.stderr}")
        return False


def main():
    """Main deployment function."""
    parser = argparse.ArgumentParser(description="Deploy database migrations")
    parser.add_argument(
        "--skip-deps", action="store_true", help="Skip dependency installation"
    )
    parser.add_argument(
        "--health-check",
        action="store_true",
        help="Run comprehensive database health check after migrations",
    )

    args = parser.parse_args()

    logger.info("Starting database deployment...")

    # Check environment variables
    if not check_environment():
        sys.exit(1)

    # Install dependencies unless skipped
    if not args.skip_deps:
        if not install_dependencies():
            sys.exit(1)

    # Full deployment process
    steps = [
        ("Check Migration Status", check_migration_status),
        ("Run Migrations", run_migrations),
    ]

    # Add health check if requested
    if args.health_check:
        steps.append(("Database Health Check", run_health_check))

    for step_name, step_func in steps:
        logger.info(f"Step: {step_name}")
        if not step_func():
            logger.error(f"Failed at step: {step_name}")
            sys.exit(1)

    logger.info("Database deployment completed successfully!")
    logger.info("All migrations applied!")


if __name__ == "__main__":
    main()
