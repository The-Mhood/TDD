#!/usr/bin/env python3
"""Regression tests for the Mac Unreal automation report parser."""

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PARSER = ROOT / "Tools/engine/parse_automation_report.py"


class AutomationReportParserTests(unittest.TestCase):
    def run_parser(self, report, log_text):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            report_path = directory / "index.json"
            log_path = directory / "automation.log"
            if report is not None:
                report_path.write_bytes(b"\xef\xbb\xbf" + json.dumps(report).encode("utf-8"))
            log_path.write_text(log_text, encoding="utf-8")
            command = ["python3", str(PARSER), "--log", str(log_path)]
            if report is not None:
                command.extend(["--report", str(report_path)])
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            return result.stdout.strip()

    def test_bom_report_and_log_count_two_successful_tests(self):
        report = {"tests": [
            {"fullTestPath": "TDD.Foundation.GameModeClass", "state": "Success"},
            {"fullTestPath": "TDD.Movement.DodgeDistanceMath", "state": "Success"},
        ]}
        log = """LogAutomationCommandLine: Found 2 automation tests based on 'TDD'
LogAutomationController: Test Started. Name=TDD.Foundation.GameModeClass
LogAutomationController: Test Started. Name=TDD.Movement.DodgeDistanceMath
"""
        self.assertEqual(self.run_parser(report, log), "2\t2\t2\t2\t0\t0")

    def test_counts_failure_and_unclassified_results_separately(self):
        report = {"tests": [
            {"fullTestPath": "TDD.One", "state": "Success"},
            {"fullTestPath": "TDD.Two", "state": "Fail"},
            {"fullTestPath": "TDD.Three", "state": "NotRun"},
        ]}
        log = """Found 3 automation tests based on 'TDD'
LogAutomationController: Test Started. Name=TDD.One
LogAutomationController: Test Started. Name=TDD.Two
LogAutomationController: Test Started. Name=TDD.Three
"""
        self.assertEqual(self.run_parser(report, log), "3\t3\t2\t1\t1\t1")

    def test_log_fallback_counts_terminal_results(self):
        log = """Found 1 automation test based on 'TDD'
LogAutomationController: Test Started. Name=TDD.One
LogAutomationController: Test Completed. Result={Passed} Name=TDD.One
"""
        self.assertEqual(self.run_parser(None, log), "1\t1\t1\t1\t0\t0")

    def test_mac_run_log_format_counts_both_started_and_completed(self):
        # Format transcribed from the owner's 2026-11-18 Mac automation log.
        log = """Found 2 automation tests based on 'TDD'
Test Started for TDD.Foundation.GameModeClass
Test Completed. Result={Success} for TDD.Foundation.GameModeClass
Test Started for TDD.Movement.DodgeDistanceMath
Test Completed. Result={Success} for TDD.Movement.DodgeDistanceMath
"""
        self.assertEqual(self.run_parser(None, log), "2\t2\t2\t2\t0\t0")


if __name__ == "__main__":
    unittest.main()
