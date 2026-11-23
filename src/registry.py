"""Чтение манифеста latest напрямую из HTTP-реестра npm."""

import json
from urllib.parse import quote
from urllib.request import urlopen


def npm_dependencies(repository, package):
    """Получить секцию dependencies опубликованного манифеста."""
    url = f"{repository.rstrip('/')}/{quote(package, safe='@')}/latest"
    with urlopen(url, timeout=15) as response:
        manifest = json.load(response)
    if not isinstance(manifest, dict):
        raise ValueError(f"{package}: ожидался JSON-объект манифеста")
    dependencies = manifest.get("dependencies", {})
    if not isinstance(dependencies, dict) or not all(
        isinstance(spec, str) for spec in dependencies.values()
    ):
        raise ValueError(f"{package}: некорректное поле dependencies")
    return dependencies
