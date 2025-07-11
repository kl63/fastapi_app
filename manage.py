#!/usr/bin/env python
import click
import subprocess
import sys
import os
import asyncio
from dotenv import load_dotenv
import uvicorn

# Load environment variables
load_dotenv()

# Add the current directory to the path so we can import our app
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.db_init import init_db


@click.group()
def cli():
    """Management script for the FastAPI User Management application."""
    pass


@cli.command()
def run():
    """Run the application server."""
    click.echo("Starting application server...")
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )


@cli.command()
def init_database():
    """Initialize the database with tables and admin user."""
    click.echo("Initializing database...")
    asyncio.run(init_db())
    click.echo("Database initialized successfully!")


@cli.command()
@click.argument("message", required=True)
def migrate(message):
    """Create a new migration with Alembic."""
    click.echo(f"Creating migration: {message}")
    subprocess.run(["alembic", "revision", "--autogenerate", "-m", message])
    click.echo("Migration created! Run 'python manage.py upgrade' to apply.")


@cli.command()
@click.option("--revision", default="head", help="Revision to upgrade to (default: head)")
def upgrade(revision):
    """Upgrade database to a specified revision (default: head)."""
    click.echo(f"Upgrading database to {revision}...")
    subprocess.run(["alembic", "upgrade", revision])
    click.echo("Database upgrade complete!")


@cli.command()
@click.option("--revision", default="-1", help="Revision to downgrade to (default: -1)")
def downgrade(revision):
    """Downgrade database to a specified revision (default: -1)."""
    click.echo(f"Downgrading database to {revision}...")
    subprocess.run(["alembic", "downgrade", revision])
    click.echo("Database downgrade complete!")


@cli.command()
def history():
    """Show migration history."""
    click.echo("Migration history:")
    subprocess.run(["alembic", "history"])


@cli.command()
def current():
    """Show current migration revision."""
    click.echo("Current revision:")
    subprocess.run(["alembic", "current"])


if __name__ == "__main__":
    cli()
