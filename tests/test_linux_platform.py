import tempfile
import unittest
from pathlib import Path
import sys
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bypass_pucit.platforms.linux import LinuxProxyManager


class LinuxPlatformTests(unittest.TestCase):
    def test_apply_and_unset_update_expected_files(self):
        temp_home = Path(tempfile.mkdtemp())
        temp_apt = temp_home / "95bypass-pucit-proxy"
        temp_env = temp_home / "environment"
        runner_calls = []

        def fake_runner(command, check=True):
            runner_calls.append(command)

        def fake_getpwnam(username):
            return SimpleNamespace(pw_dir=str(temp_home), pw_shell="/bin/zsh")

        def fake_command_exists(name):
            return name in {"git", "npm", "yarn", "apt-get", "pnpm", "snap"}

        with patch("bypass_pucit.platforms.linux.os.environ", {"SUDO_USER": "alice"}), \
            patch("bypass_pucit.platforms.linux.pwd.getpwnam", side_effect=fake_getpwnam), \
            patch("bypass_pucit.platforms.linux.command_exists", side_effect=fake_command_exists), \
            patch("bypass_pucit.platforms.linux.python_module_exists", return_value=True), \
            patch("bypass_pucit.platforms.linux.print_info", lambda message: None), \
            patch.object(LinuxProxyManager, "_environment_path", lambda self: temp_env):
            manager = LinuxProxyManager("http://proxy.local:8080", runner=fake_runner)
            manager._apt_proxy_path = lambda: temp_apt

            report = manager.apply()

            self.assertTrue((temp_home / ".zshrc").exists())
            self.assertTrue(temp_env.exists())
            self.assertTrue((temp_home / ".config" / "pip" / "pip.conf").exists())
            self.assertTrue((temp_home / ".wgetrc").exists())
            self.assertTrue((temp_home / ".m2" / "settings.xml").exists())
            self.assertTrue((temp_home / ".gradle" / "gradle.properties").exists())
            self.assertTrue((temp_home / ".docker" / "config.json").exists())
            self.assertTrue(temp_apt.exists())
            self.assertIn("git", report.applied)
            self.assertIn("npm", report.applied)
            self.assertIn("yarn", report.applied)
            self.assertIn("pnpm", report.applied)
            self.assertIn("wget", report.applied)
            self.assertIn("maven", report.applied)
            self.assertIn("gradle", report.applied)
            self.assertIn("docker", report.applied)
            self.assertIn("snap", report.applied)
            self.assertIn("apt", report.applied)
            self.assertEqual(runner_calls[0], ["git", "config", "--global", "http.proxy", "http://proxy.local:8080"])

            runner_calls.clear()
            report = manager.unset()

            self.assertFalse((temp_home / ".zshrc").exists())
            self.assertFalse(temp_env.exists())
            self.assertFalse((temp_home / ".config" / "pip" / "pip.conf").exists())
            self.assertFalse((temp_home / ".wgetrc").exists())
            self.assertFalse((temp_home / ".m2" / "settings.xml").exists())
            self.assertFalse((temp_home / ".gradle" / "gradle.properties").exists())
            self.assertFalse((temp_home / ".docker" / "config.json").exists())
            self.assertFalse(temp_apt.exists())
            self.assertIn(["git", "config", "--global", "--unset", "http.proxy"], runner_calls)
            self.assertIn(["npm", "config", "delete", "proxy"], runner_calls)
            self.assertIn(["yarn", "config", "delete", "proxy"], runner_calls)
            self.assertIn(["pnpm", "config", "delete", "proxy"], runner_calls)
