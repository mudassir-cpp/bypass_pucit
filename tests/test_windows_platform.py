import tempfile
import unittest
from pathlib import Path
import sys
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bypass_pucit.platforms.windows import WindowsProxyManager


class WindowsPlatformTests(unittest.TestCase):
    def test_apply_and_unset_build_expected_commands(self):
        runner_calls = []
        temp_home = Path(tempfile.mkdtemp())

        def fake_runner(command, check=True):
            runner_calls.append(command)

        def fake_command_exists(name):
            return name in {"reg", "netsh", "pnpm"}

        with patch("bypass_pucit.platforms.windows.command_exists", side_effect=fake_command_exists), \
            patch("bypass_pucit.platforms.windows.WindowsProxyManager.broadcast_environment_change", lambda self: None), \
            patch("bypass_pucit.platforms.windows.Path.home", return_value=temp_home):
            manager = WindowsProxyManager("http://proxy.local:8080", runner=fake_runner)
            report = manager.apply()

            self.assertIn("internet-settings", report.applied)
            self.assertIn("environment", report.applied)
            self.assertIn("wget", report.applied)
            self.assertIn("maven", report.applied)
            self.assertIn("gradle", report.applied)
            self.assertIn("docker", report.applied)
            self.assertIn("pnpm", report.applied)
            self.assertIn("winhttp", report.applied)
            self.assertTrue((temp_home / ".wgetrc").exists())
            self.assertTrue((temp_home / ".m2" / "settings.xml").exists())
            self.assertTrue((temp_home / ".gradle" / "gradle.properties").exists())
            self.assertTrue((temp_home / ".docker" / "config.json").exists())
            self.assertEqual(runner_calls[0][0:3], ["reg", "add", r"HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings"])
            self.assertIn(["pnpm", "config", "set", "proxy", "http://proxy.local:8080"], runner_calls)
            self.assertIn(["netsh", "winhttp", "set", "proxy", 'proxy-server="http://proxy.local:8080"', 'bypass-list="localhost;127.0.0.1;::1"'], runner_calls)

            runner_calls.clear()
            report = manager.unset()

            self.assertIn("internet-settings", report.applied)
            self.assertIn("environment", report.applied)
            self.assertIn("wget", report.applied)
            self.assertIn("maven", report.applied)
            self.assertIn("gradle", report.applied)
            self.assertIn("docker", report.applied)
            self.assertIn("pnpm", report.applied)
            self.assertIn("winhttp", report.applied)
            self.assertFalse((temp_home / ".wgetrc").exists())
            self.assertFalse((temp_home / ".m2" / "settings.xml").exists())
            self.assertFalse((temp_home / ".gradle" / "gradle.properties").exists())
            self.assertFalse((temp_home / ".docker" / "config.json").exists())
            self.assertIn(["pnpm", "config", "delete", "proxy"], runner_calls)
            self.assertIn(["netsh", "winhttp", "reset", "proxy"], runner_calls)
