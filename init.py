import ascend
import fileinput
import os
import sys

from ascend.sdk.client import Client
from ascend.sdk.render import download_dataflow


def replace(file, searchExp, replaceExp):
    for line in fileinput.input(file, inplace=True):
        line = line.replace(searchExp, replaceExp)
        sys.stdout.write(line)


def main():
    hostname = input('Enter the name of the hostname: ')
    dataserv = input('Enter the name of the data service: ').replace(' ', '_')
    dataflow = input('Enter the name of the data flow: ').replace(' ', '_')

    client = Client(hostname=hostname)
    download_dataflow(client, data_service_id=dataserv, dataflow_id=dataflow, resource_base_path='.')
    os.rename(f'{dataflow}.py', 'upload.py')
    replace('upload.py', f'client = Client("{hostname}")',
            'client = Client(hostname=os.getenv("ASCEND_HOSTNAME"))')
    replace('.github/workflows/main.yml', '<<replace_env>>', hostname)


main()

