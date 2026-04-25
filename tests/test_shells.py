import unittest
from pathlib import Path

from bypass_pucit.shells import detect_shell_name, shell_profile_path


class ShellsTests(unittest.TestCase):
    def test_detect_shell_name_normalizes_known_shells(self):
        self.assertEqual(detect_shell_name(shell_value="/usr/bin/fish"), "fish")
        self.assertEqual(detect_shell_name(shell_value="/usr/bin/xonsh"), "xonsh")
        self.assertEqual(detect_shell_name(shell_value=r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"), "powershell")

    def test_shell_profile_path_supports_new_shells(self):
        home = Path("/tmp/user")
        self.assertEqual(shell_profile_path(home, "fish"), home / ".config" / "fish" / "config.fish")
        self.assertEqual(shell_profile_path(home, "xonsh"), home / ".xonshrc")
        self.assertEqual(shell_profile_path(home, "powershell"), home / ".config" / "powershell" / "Microsoft.PowerShell_profile.ps1")
        self.assertEqual(shell_profile_path(home, "custom-shell"), home / ".profile")
