"""Command line utilities."""
import os

import requests
import typer
from rich.console import Console
from rich.progress import (BarColumn, DownloadColumn, Progress, TextColumn,
                           TimeRemainingColumn, TransferSpeedColumn)

app = typer.Typer()
console = Console()


def download_file_from_google_drive(file_id, destination):
    """Downloads a file from Google Drive using its file ID.

    Parameters
    ----------
    file_id: str
        The ID of the file on Google Drive.
    destination: str
        The local path where the file should be saved.

    Returns
    -------
    The local path where the file should be saved.
    """

    # pylint: disable=invalid-name
    def save_response_content(response, destination):
        """Saves the content of a response to a file.

        Parameters
        ----------
        response: requests.Response
            The response to save.
        destination: str
            The local path where the file should be saved.
        """
        CHUNK_SIZE = 32768
        total_size = int(response.headers.get('content-length', 0))
        with Progress(
            TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
            BarColumn(bar_width=None),
            "[progress.percentage]{task.percentage:>3.1f}%",
            "•",
            DownloadColumn(),
            "•",
            TransferSpeedColumn(),
            "•",
            TimeRemainingColumn(),
            console=console
        ) as progress:
            task_id = progress.add_task(
                "download", filename=os.path.basename(destination), total=total_size)
            with open(destination, "wb") as f:
                for chunk in response.iter_content(CHUNK_SIZE):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
                        progress.update(task_id, advance=len(chunk))

    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params={'id': file_id}, stream=True)
    params = {'id': file_id}
    response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)


@app.command()
def download(name: str):
    """Download a file.

    Parameters
    ----------
    name: str
        The name of the file to download (currently supports 'jmdict').
    """
    data_dir = os.path.join(os.path.dirname(__file__), '../data')
    os.makedirs(data_dir, exist_ok=True)

    match name:
        case 'jmdict':
            file_id = "1dlvguHuMjDmtpA4beu1WaVbDte5j4SLk"
            destination = os.path.join(data_dir, "JMdict_en.gz")
            download_file_from_google_drive(file_id, destination)
        case 'xlwsd':
            file_id = "1d75OUrM3dyAvYUsnBXle-Z1W0NHyKIBD"
            destination = os.path.join(data_dir, "xl-wsd-data.zip")
            download_file_from_google_drive(file_id, destination)
        case _:
            print(f"Error: Unknown file name '{name}'.")


if __name__ == "__main__":
    app()
