#!/usr/bin/env python3
"""Simple automation script combining Nmap and OpenVAS scans.

This script is a basic example showing how to chain Nmap discovery with
OpenVAS (GVM) vulnerability scans. It assumes you have Nmap and
OpenVAS/GVM installed and that `gvm-cli` is available on your system.

Use only on hosts and networks you own or have explicit permission to
scan.
"""

import argparse
import subprocess
from pathlib import Path
from datetime import datetime


def run_nmap(target: str, output_dir: Path) -> Path:
    """Run Nmap against the target and return the XML output file path."""
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    xml_file = output_dir / f"nmap_{target}_{timestamp}.xml"
    cmd = ["nmap", "-sS", "-sV", "-oX", str(xml_file), target]
    print("Running Nmap:", " ".join(cmd))
    subprocess.run(cmd, check=True)
    return xml_file


def run_openvas(xml_file: Path, target_name: str, gmp_username: str, gmp_password: str):
    """Import the Nmap results into OpenVAS and start a scan.

    This uses `gvm-cli` with XML commands. Adjust connection parameters and
    commands as needed for your environment.
    """
    create_target_xml = (
        f"<create_target><name>{target_name}</name>"
        f"<hosts>{target_name}</hosts></create_target>"
    )
    cmd_create = [
        "gvm-cli",
        "socket",
        "--xml",
        create_target_xml,
    ]
    print("Creating target in OpenVAS:", " ".join(cmd_create))
    subprocess.run(cmd_create, check=True)
    # Additional steps would include creating a scan task and starting it.
    # Refer to OpenVAS documentation for full automation details.


def main():
    parser = argparse.ArgumentParser(description="Automate Nmap and OpenVAS scans")
    parser.add_argument("target", help="Hostname or IP address to scan")
    parser.add_argument(
        "--output-dir",
        default="scan_results",
        help="Directory to store scan results",
    )
    parser.add_argument("--username", required=True, help="OpenVAS username")
    parser.add_argument("--password", required=True, help="OpenVAS password")

    args = parser.parse_args()
    output_dir = Path(args.output_dir)
    xml_report = run_nmap(args.target, output_dir)
    run_openvas(xml_report, args.target, args.username, args.password)


if __name__ == "__main__":
    main()
