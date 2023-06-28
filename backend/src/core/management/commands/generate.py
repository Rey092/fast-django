# -*- coding: utf-8 -*-
"""Module for app generation."""
import logging
import os

from django.core.management import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Command for app generation."""

    def handle(self, test_mode=False, *args, **options):
        """Handle command."""
        app_name = input("Enter the app name: ").lower()
        models = input("Enter the name of the models separated by commas: ")
        model_list = models.split(",")
        model_list = [model.strip() for model in model_list]

        # Create the Django app directory in the src folder
        os.system(f"mkdir -p src/{app_name}")
        os.system(f"django-admin startapp {app_name} src/{app_name}")

        # Add 'src.' to the app name in the apps.py file
        with open(f"src/{app_name}/apps.py", "w") as f:
            f.write("from django.apps import AppConfig\n\n")
            f.write(f"class {app_name.capitalize()}Config(AppConfig):\n")
            f.write("\tdefault_auto_field = 'django.db.models.BigAutoField'\n")
            f.write(f"\tname = 'src.{app_name}'\n")

        # Create the endpoints.py and containers.py files
        with open(f"src/{app_name}/endpoints.py", "w") as f:
            f.write("# Add endpoints here\n")
        with open(f"src/{app_name}/containers.py", "w") as f:
            f.write("# Add containers here\n")

        # Create the services and repositories packages
        os.system(f"mkdir -p src/{app_name}/services")
        os.system(f"mkdir -p src/{app_name}/repositories")

        # Create the __init__.py files
        with open(f"src/{app_name}/repositories/__init__.py", "w") as f:
            f.write("# -*- coding: utf-8 -*-\n")
            f.write(f'"""Initiate {app_name} app."""\n')
        with open(f"src/{app_name}/services/__init__.py", "w") as f:
            f.write("# -*- coding: utf-8 -*-\n")
            f.write(f'"""Initiate {app_name} app."""\n')

        # Create the models.py file and add the models, services, and repositories to it
        with open(f"src/{app_name}/models.py", "w") as f:
            f.write("# -*- coding: utf-8 -*-\n")
            f.write(f'"""Initiate {app_name} models app."""\n')
            f.write("from django.db import models\n\n\n")
            for model in model_list:
                f.write(f"class {model}(models.Model):\n")
                f.write("\tname = models.CharField(max_length=100)\n")
                f.write("\t# Add more fields here\n\n\n")

        # add model registration to admin.py
        with open(f"src/{app_name}/admin.py", "w") as f:
            f.write("# -*- coding: utf-8 -*-\n")
            f.write(f'"""Initiate {app_name} admin app."""\n')
            f.write("from django.contrib import admin\n\n")
            for model in model_list:
                f.write(f"from src.{app_name}.models import {model}\n")
            f.write("\n\n")
            for model in model_list:
                f.write(f"admin.site.register({model})\n")

        # add 'src.*app_name*' to django settings on next row after 'LOCAL_APPS'
        with open("config/settings.py", "r") as f:
            settings = f.read()
        with open("config/settings.py", "w") as f:
            f.write(settings.replace("LOCAL_APPS = [", f'LOCAL_APPS = [\n\t"src.{app_name}",'))

        # delete 'tests.py' and 'views.py' files in the app directory
        os.system(f"rm src/{app_name}/tests.py")
        os.system(f"rm src/{app_name}/views.py")

        # for each model, create a service and repository file.
        for model in model_list:
            # change camel case to snake case
            model_snake = "".join(["_" + i.lower() if i.isupper() else i for i in model]).lstrip("_")

            # create service file
            with open(f"src/{app_name}/services/{model_snake}.py", "w") as f:
                f.write("# -*- coding: utf-8 -*-\n")
                f.write(f'"""{model} service."""\n')
                f.write("from base.services import BaseService\n")
                f.write(f"from src.{app_name}.repositories.{model_snake} import {model}Repository\n\n\n")
                f.write(f"class {model}Service(BaseService):\n")
                f.write(f"\tdef __init__(self, {model_snake}_repository: {model}Repository):\n")
                f.write(f"\t\tself.repository: {model}Repository = {model_snake}_repository\n")

            # repository creation
            with open(f"src/{app_name}/repositories/{model_snake}.py", "w") as f:
                f.write("# -*- coding: utf-8 -*-\n")
                f.write(f'"""{model} repository."""\n')
                f.write("from base.repositories import BaseRepository\n")
                f.write(f"from src.{app_name}.models import {model}\n\n\n")
                f.write(f"class {model}Repository(BaseRepository):\n")
                f.write("\tdef __init__(self):\n")
                f.write(f"\t\tself.model = {model}\n")

        # create container file
        with open(f"src/{app_name}/containers.py", "w") as f:
            f.write("# -*- coding: utf-8 -*-\n")
            f.write(f'"""{app_name} container module."""\n')
            f.write("from dependency_injector import containers, providers\n")
            for model in model_list:
                model_snake = "".join(["_" + i.lower() if i.isupper() else i for i in model]).lstrip("_")
                f.write(f"from src.{app_name}.repositories.{model_snake} import {model}Repository\n")
                f.write(f"from src.{app_name}.services.{model_snake} import {model}Service\n\n")
            f.write("\n")
            f.write(f"class {app_name.capitalize()}Container(containers.DeclarativeContainer):\n")
            f.write(f'\t"""{app_name.capitalize()} container."""\n\n')
            for model in model_list:
                model_snake = "".join(["_" + i.lower() if i.isupper() else i for i in model]).lstrip("_")
                f.write(
                    f"\t{model_snake}_repository: {model}Repository = providers.Singleton(\n\t\t{model}"
                    f"Repository\n\t)\n"
                )
                f.write(
                    f"\t{model_snake}_service: {model}Service = providers.Singleton(\n\t\t{model}Service, "
                    f"{model_snake}_repository={model_snake}_repository\n\t)\n"
                )

        # create schemas folder and file
        os.mkdir(f"src/{app_name}/schemas")
        with open(f"src/{app_name}/schemas/{app_name}.py", "w") as f:
            f.write("# -*- coding: utf-8 -*-\n")
            f.write(f'"""{app_name} schemas."""\n')
            f.write("from pydantic import BaseModel\n\n\n")
            f.write(f"class {model}Schema(BaseModel):\n")
            f.write(f'\t"""{model} schema."""\n\n')
            f.write("\tname: str\n")

        # create sample in entrypoint.py
        model_snake = "".join(["_" + i.lower() if i.isupper() else i for i in model_list[0]]).lstrip("_")

        with open(f"src/{app_name}/endpoints.py", "w") as f:
            f.write("# -*- coding: utf-8 -*-\n")
            f.write(f'"""{app_name} module endpoints."""\n')
            f.write("from typing import List\n\n")
            f.write("from dependency_injector.wiring import Provide, inject\n")
            f.write("from fastapi import APIRouter, Depends\n")
            f.write("from src.authentication.dependencies import get_authenticated_user_payload\n")
            f.write("from src.authentication.schemas.auth import UserPayload\n")
            f.write("from src.dependencies.containers import Registry\n")
            f.write(f"from src.{app_name}.models import {model}\n")
            f.write(f"from src.{app_name}.schemas.{app_name} import {model}Schema\n")
            f.write(f"from src.{app_name}.services.{model_snake} import {model}Service\n")
            f.write("from starlette import status\n")
            f.write("from utils.responses.examples_generator import generate_examples\n")
            f.write("from utils.responses.http.api import NotFoundException\n\n\n")
            f.write(f'{app_name}_router = APIRouter(prefix="/{app_name}", tags=["{app_name.capitalize()}"])\n\n')
            f.write(f"@{app_name}_router.get(\n")
            f.write('\t"/",\n')
            f.write(f'\tname="{app_name}:get",\n')
            f.write(f'\tsummary="Get current {app_name}",\n')
            f.write(
                f'\tdescription="Get current {app_name}. '
                f'NotFoundException can be raised only if server is not configured properly.",\n'
            )
            f.write("\tstatus_code=status.HTTP_200_OK,\n")
            f.write(f"\tresponse_model=List[{model}Schema],\n")
            f.write("\tresponses=generate_examples(\n")
            f.write("\t\tNotFoundException,\n")
            f.write("\t\tauth=True,\n")
            f.write("\t),\n")
            f.write(")\n")
            f.write("@inject\n")
            f.write(f"async def get_{app_name}(\n")
            f.write("\tuser_payload: UserPayload = Depends(get_authenticated_user_payload),\n")
            f.write(
                f"\t{app_name}_service: {model}Service = "
                f"Depends(Provide[Registry.{app_name}.{app_name}_service]),\n"
            )
            f.write("):\n")
            f.write(f'\t"""Get current {app_name}."""\n')
            f.write(f"\t{app_name}_list: List[{model}] = await {app_name}_service.get_all()\n")
            f.write(f"\treturn {app_name}_list\n")
