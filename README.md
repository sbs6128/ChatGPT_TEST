# ChatGPT_TEST

This repository demonstrates simple automation of vulnerability scans using
Nmap and OpenVAS (GVM). The `vuln_scan.py` script runs an Nmap scan and then
triggers an OpenVAS scan using `gvm-cli`.

## Usage

1. Install Nmap and OpenVAS on your system. Ensure `gvm-cli` is available.
2. Run the script with the target host and your OpenVAS credentials:

```bash
python3 vuln_scan.py example.com --username YOUR_USER --password YOUR_PASS
```

Scan results are stored under `scan_results/`.

**Important:** Use this tool only on systems you own or have explicit
permission to test.
