from pathlib import Path
from typing import Dict

from app.settings import settings


async def get_file_paths() -> Dict[str, Path]:
    file_paths = {}
    for file_sample in settings.FILES_DIR.iterdir():
        extension = "".join(file_sample.suffixes).removeprefix(".")
        file_paths[extension] = file_sample
    return file_paths
