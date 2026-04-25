import unittest
from pathlib import Path
import sys
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bypass_pucit.cli import main


class CliTests(unittest.TestCase):
    def test_help_without_arguments(self):
        with patch("bypass_pucit.cli.print_help") as print_help:
            code = main([])

        self.assertEqual(code, 0)
        print_help.assert_called_once()

    def test_unsupported_platform_returns_error(self):
        with patch("bypass_pucit.manager.platform.system", return_value="Darwin"), \
            patch("bypass_pucit.cli.print_error") as print_error:
            code = main(["set"])

        self.assertEqual(code, 1)
        print_error.assert_called_once()
