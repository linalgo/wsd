import os

from linalgo.hub.client import LinalgoClient

LINHUB_TOKEN = os.getenv('LINHUB_TOKEN')
LINHUB_URL = os.getenv('LINHUB_URL')
LINHUB_TASK = os.getenv('LINHUB_TASK')

client = LinalgoClient(api_url=LINHUB_URL, token=LINHUB_TOKEN)
task = client.get_task(LINHUB_TASK, lazy=True)

print(task)