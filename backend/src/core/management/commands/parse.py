# -*- coding: utf-8 -*-
"""Module for the management command 'init_project'. Sync version."""
import logging

from django.core.management import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Command for basic data initialization."""

    def handle(self, test_mode=False, *args, **options):
        """Handle command."""
        from src.core.tasks import parse_future_releases_task

        parse_future_releases_task()
