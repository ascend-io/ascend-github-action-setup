#!/usr/bin/env python3

import ascend
import fileinput
import os
import shutil
import sys
import typer

from ascend.sdk.client import Client
from ascend.sdk.render import download_dataflow, download_data_service

app = typer.Typer()


def replace(file, searchExp, replaceExp):
    for line in fileinput.input(file, inplace=True):
        line = line.replace(searchExp, replaceExp)
        sys.stdout.write(line)


@app.command()
def create_dataflow(
        hostname: str,
        data_service_id: str,
        dataflow_id: str):
    """
    Download dataflow locally
    """
    dataserv = data_service_id.replace('-', '_').replace(' ', '__')
    dataflow = dataflow_id.replace('-', '_').replace(' ', '__')

    client = Client(hostname=hostname)
    download_dataflow(client, data_service_id=dataserv, dataflow_id=dataflow, resource_base_path='.')
    os.rename(f'{dataflow}.py', 'upload.py')
    replace('upload.py', f'client = Client("{hostname}")',
            'client = Client(hostname=os.getenv("ASCEND_HOSTNAME"))')

    shutil.copy('.github/workflows/main.yml.template',
        '.github/workflows/main.yml')
    replace('.github/workflows/main.yml', '<<replace_env>>', hostname)


@app.command()
def create_data_service(
        hostname: str,
        data_service_id: str):
    """
    Download data service locally
    """
    dataserv = data_service_id.replace('-', '_').replace(' ', '__')

    client = Client(hostname=hostname)
    download_data_service(client, data_service_id=dataserv, resource_base_path='.')
    os.rename(f'{dataserv}.py', 'upload.py')
    replace('upload.py', f'client = Client("{hostname}")',
            'client = Client(hostname=os.getenv("ASCEND_HOSTNAME"))')

    shutil.copy('.github/workflows/main.yml.template',
        '.github/workflows/main.yml')
    replace('.github/workflows/main.yml', '<<replace_env>>', hostname)


if __name__ == "__main__":
    app()
