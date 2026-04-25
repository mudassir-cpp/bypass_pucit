import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from bypass_pucit.platforms.linux import LinuxProxyManager


class VerboseTests(unittest.TestCase):
    def test_verbose_mode_emits_progress_for_shell_file(self):
        temp_home = Path(tempfile.mkdtemp())
        logs = []

        def fake_getpwnam(username):
            return SimpleNamespace(pw_dir=str(temp_home), pw_shell="/bin/fish")

        with patch("bypass_pucit.platforms.linux.os.environ", {"SUDO_USER": "alice"}), \
            patch("bypass_pucit.platforms.linux.pwd.getpwnam", side_effect=fake_getpwnam), \
            patch("bypass_pucit.platforms.linux.command_exists", return_value=False), \
            patch("bypass_pucit.platforms.linux.python_module_exists", return_value=False), \
            patch("bypass_pucit.platforms.linux.print_info", side_effect=lambda message: logs.append(message)):
            manager = LinuxProxyManager("http://proxy.local:8080", verbose=True)
            manager._environment_path = lambda: temp_home / "environment"
            manager.apply()

        self.assertTrue(any("Detected shell profile" in message for message in logs))
        self.assertTrue(any("Writing shell profile" in message for message in logs))
