"""Командная строка анализатора зависимостей npm."""

import argparse
import re
from pathlib import Path
from urllib.parse import urlsplit

from registry import npm_dependencies


NPM_NAME = r"(?:@[a-z0-9._-]+/)?[a-z0-9][a-z0-9._-]*"
TEST_NAME = r"[A-Z]+"


def valid_url(value):
    """Проверить URL HTTP(S) с необязательным префиксом пути."""
    try:
        parts = urlsplit(value)
        parts.port
    except ValueError:
        return False
    return (
        parts.scheme in ("http", "https")
        and bool(parts.hostname)
        and not any(char.isspace() for char in value)
        and parts.username is None
        and not parts.query
        and not parts.fragment
    )


def parse_args(argv=None):
    """Прочитать и проверить параметры пользователя."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", required=True, help="имя пакета")
    parser.add_argument("--repo", required=True, help="URL или путь к JSON")
    parser.add_argument("--test", action="store_true", help="тестовый JSON")
    parser.add_argument("--ascii", action="store_true", help="ASCII-дерево")
    parser.add_argument("--filter", metavar="TEXT", help="исключить по имени")
    args = parser.parse_args(argv)
    pattern = TEST_NAME if args.test else NPM_NAME
    if not re.fullmatch(pattern, args.package):
        parser.error("--package: недопустимое имя пакета")
    if args.test and not Path(args.repo).is_file():
        parser.error("--repo: файл тестового репозитория не найден")
    if not args.test and not valid_url(args.repo):
        parser.error("--repo: требуется корректный URL HTTP(S)")
    if args.filter is not None and not args.filter.strip():
        parser.error("--filter: подстрока должна быть непустой")
    return args


def main():
    """Запустить приложение."""
    args = parse_args()
    if args.test:
        raise SystemExit("Тестовый репозиторий появится на следующем этапе.")
    try:
        dependencies = npm_dependencies(args.repo, args.package)
    except (OSError, ValueError) as error:
        raise SystemExit(f"Ошибка реестра: {error}") from None
    for name, spec in sorted(dependencies.items()):
        print(f"{name} {spec}")


if __name__ == "__main__":
    main()
