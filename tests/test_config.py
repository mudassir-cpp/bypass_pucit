import unittest
from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bypass_pucit.config import DEFAULT_PROXY, load_proxy_url


class ConfigTests(unittest.TestCase):
    def test_load_proxy_url_uses_explicit_value(self):
        self.assertEqual(load_proxy_url("http://proxy.local:8080"), "http://proxy.local:8080")

    def test_load_proxy_url_falls_back_to_default(self):
        self.assertEqual(load_proxy_url(None), DEFAULT_PROXY)
