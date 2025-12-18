"""
End-to-end tests for Anonym tool using approvaltests.
Tests the passing test cases from tests.sh
"""
import subprocess
import os
import pytest
import shutil
from pathlib import Path
from approvaltests import verify


# Get the test directory
TEST_DIR = Path(__file__).parent.parent
PROJECT_ROOT = TEST_DIR.parent
OUTPUT_DIR = TEST_DIR / "output"


def run_anonym(args):
    """Run anonym.py with given arguments and return stdout + stderr"""
    cmd = ["python", str(PROJECT_ROOT / "anonym.py")] + args.split()
    result = subprocess.run(
        cmd,
        cwd=str(TEST_DIR),
        capture_output=True,
        text=True,
    )
    return result.stdout + result.stderr


def setup_output_dir():
    """Prepare output directory for tests"""
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(exist_ok=True)


class TestE2EAnonym:
    """End-to-end tests for Anonym tool"""

    def setup_method(self):
        """Setup before each test"""
        setup_output_dir()

    def test_simple_csv(self):
        """Test simple CSV anonymization"""
        output = run_anonym(
            "-p -o output -Fe email -Fn name -Fu id -Fi ip -Fh host -Fc long -Fc lat input/simple-csv.csv"
        )
        verify(output)

    def test_simple_csv_2_files(self):
        """Test simple CSV anonymization with 2 files"""
        output = run_anonym(
            "-p -o output -Fe email -Fn name -Fu id -Fi ip -Fh host -Fc long -Fc lat input/simple-csv.csv input/simple-csv-2.csv"
        )
        verify(output)

    def test_bad_pattern(self):
        """Test handling of bad pattern"""
        output = run_anonym(
            "-o output -Fn json.' input/csv-json.csv"
        )
        verify(output)

    # def test_bad_pattern_verbose(self):
    #     """Test handling of bad pattern with verbose output"""
    #     output = run_anonym(
    #         "-v -o output -Fn json.' input/csv-json.csv"
    #     )
    #     verify(output)

    def test_header_not_found(self):
        """Test handling of missing headers"""
        output = run_anonym(
            "-o output -Fn badname1 -Fh badname2 input/csv-json.csv"
        )
        verify(output)

    def test_csv_with_json(self):
        """Test CSV with embedded JSON"""
        output = run_anonym(
            '-p -o output -t csv -Fe json.a -Fu json.b -Fn json2.$[?(@.a=="1")].b -Fh json2.$[?(@.a=="2")].b input/csv-json.csv'
        )
        verify(output)

    def test_simple_json(self):
        """Test simple JSON anonymization"""
        output = run_anonym(
            '-p -o output -t json -Fn a.b -Fu x -Fh $.array[?(@.a=="1")].b input/simple-json.json'
        )
        verify(output)

    def test_bad_coord(self):
        """Test handling of bad coordinates"""
        output = run_anonym(
            "-o output -Fc test input/bad-coord.csv"
        )
        verify(output)

    def test_bad_embedded_json(self):
        """Test handling of bad embedded JSON"""
        output = run_anonym(
            "-o output -Fu test.a input/bad-embed-json.csv"
        )
        verify(output)

    def test_bad_ipv4(self):
        """Test handling of bad IPv4"""
        output = run_anonym(
            "-o output -Fi test input/bad-ipv4.csv"
        )
        verify(output)

    def test_bad_ipv6(self):
        """Test handling of bad IPv6"""
        output = run_anonym(
            "-o output -Fi test input/bad-ipv6.csv"
        )
        verify(output)

    def test_bad_json_file(self):
        """Test handling of bad JSON file"""
        output = run_anonym(
            "-o output -t json -Fi test input/bad-json.json"
        )
        verify(output)

    def test_missing_input_file(self):
        """Test handling of missing input file"""
        output = run_anonym(
            "-o output -Fi test input/missing.csv"
        )
        verify(output)

    def test_missing_output_folder(self):
        """Test handling of missing output folder"""
        output = run_anonym(
            "-o missing -Fi test input/simple-csv.csv"
        )
        verify(output)

    def test_dirty_ips(self):
        """Test handling of dirty IPs"""
        output = run_anonym(
            "-p -o output -Fi ip input/dirty-ips.csv"
        )
        verify(output)

    def test_cidr_ips(self):
        """Test handling of CIDR IPs"""
        output = run_anonym(
            "-p -o output -Fi test input/cidr-ips.csv"
        )
        verify(output)

    def test_host_names(self):
        """Test handling of host names"""
        output = run_anonym(
            "-p -o output -Fh test input/host-names.csv"
        )
        verify(output)
