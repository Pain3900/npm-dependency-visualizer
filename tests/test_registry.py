"""Проверки запроса и разбора ответа npm."""

import io
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

from src.registry import npm_dependencies


class RegistryTests(unittest.TestCase):
    @patch("src.registry.urlopen")
    def test_scoped_name_and_response(self, request):
        request.return_value = io.BytesIO(
            b'{"dependencies":{"dep":"^1.0.0"}}'
        )
        result = npm_dependencies("https://example.org/registry/", "@x/demo")
        self.assertEqual(result, {"dep": "^1.0.0"})
        request.assert_called_once_with(
            "https://example.org/registry/@x%2Fdemo/latest", timeout=15
        )

    @patch("src.registry.urlopen")
    def test_no_dependencies(self, request):
        request.return_value = io.BytesIO(b'{"name":"demo"}')
        self.assertEqual(npm_dependencies("https://example.org", "demo"), {})

    @patch("src.registry.urlopen")
    def test_missing_package(self, request):
        request.side_effect = HTTPError("", 404, "Not Found", None, None)
        with self.assertRaises(HTTPError):
            npm_dependencies("https://example.org", "missing")
