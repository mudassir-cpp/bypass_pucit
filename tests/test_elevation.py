import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bypass_pucit import elevation


class ElevationTests(unittest.TestCase):
    def test_linux_sudo_command_preserves_arguments(self):
        captured = []

        def fake_launcher(binary, command):
            captured.append((binary, command))

        with patch("bypass_pucit.elevation.shutil.which", return_value="/usr/bin/sudo"):
            result = elevation.relaunch_with_sudo(["set", "--proxy", "http://proxy"], launcher=fake_launcher)

        self.assertTrue(result)
        self.assertEqual(captured[0][0], "sudo")
        self.assertEqual(
            captured[0][1],
            ["sudo", "-E", sys.executable, "-m", "bypass_pucit.main", "set", "--proxy", "http://proxy"],
        )

    def test_windows_uac_command_uses_runas(self):
        calls = []

        class FakeShell32(object):
            def ShellExecuteW(self, *args):
                calls.append(args)
                return 33

        fake_ctypes = types.SimpleNamespace(windll=types.SimpleNamespace(shell32=FakeShell32()))

        with patch.dict(sys.modules, {"ctypes": fake_ctypes}):
            result = elevation.relaunch_with_uac(["set"])

        self.assertTrue(result)
        self.assertEqual(
            calls[0],
            (None, "runas", sys.executable, "-m bypass_pucit.main set", None, 1),
        )
