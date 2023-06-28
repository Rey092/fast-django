# -*- coding: utf-8 -*-
"""Containers module."""
import os
from typing import List

from dependency_injector import containers, providers
from django.conf import settings

from src.authentication.containers import AuthContainer
from src.core.containers import CoreContainer
from src.users.containers import UserContainer


def get_endpoints_modules() -> List[str]:
    """Get endpoints modules."""
    # for each app in LOCAL_APPS add endpoints and tests modules and files
    endpoints_modules = []

    for app in settings.LOCAL_APPS:
        # add endpoints, endpoints modules and tests modules
        endpoints_file_name = os.path.join(settings.ROOT_DIR, app.replace(".", "/"), "endpoints.py")
        tasks_file_name = os.path.join(settings.ROOT_DIR, app.replace(".", "/"), "tasks.py")
        endpoints_folder_name = os.path.join(settings.ROOT_DIR, app.replace(".", "/"), "endpoints")
        tests_folder_name = os.path.join(settings.ROOT_DIR, app.replace(".", "/"), "tests")

        # add endpoints file
        for file_name in [endpoints_file_name, tasks_file_name]:
            if os.path.exists(file_name):
                endpoints_modules.append(f"{app}.{file_name.split('/')[-1][:-3]}")

        # add endpoints and tests modules
        for folder_name in [tests_folder_name, endpoints_folder_name]:
            if os.path.exists(folder_name):
                files = os.listdir(folder_name)
                for file in files:
                    if str(file).endswith(".py"):
                        endpoints_modules.append(f"{app}.{folder_name.split('/')[-1]}.{file[:-3]}")

    return endpoints_modules


class Registry(containers.DeclarativeContainer):
    """Registry container. It is a root container for all other containers.

    It is used to provide access to all other containers from any place of the application.
    """

    wiring_config: containers.WiringConfiguration = containers.WiringConfiguration(
        modules=get_endpoints_modules(),
    )

    authentication: providers.Container[AuthContainer] = providers.Container(
        AuthContainer,
    )

    users: providers.Container[UserContainer] = providers.Container(
        UserContainer,
    )

    core: providers.Container[CoreContainer] = providers.Container(
        CoreContainer,
    )


registry = Registry()
