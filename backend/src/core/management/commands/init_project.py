# -*- coding: utf-8 -*-
"""Module for the management command 'init_project'. Sync version."""
import asyncio
import logging

from django.core.management import BaseCommand

from src.core.management.commands.init_project_async import \
    ProjectInitialization

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Command for basic data initialization."""

    def handle(self, test_mode=False, *args, **options):
        """Handle command."""
        from config_fastapi.app import app_fastapi

        loop = asyncio.new_event_loop()
        loop.run_until_complete(ProjectInitialization.start(app_fastapi))
