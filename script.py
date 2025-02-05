import requests
import json
import argparse
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def find_subdomains(domain, output_file="output.txt"):
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    headers = {"User-Agent": "Mozilla/5.0"}

    # Configure retries
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=5, status_forcelist=[500, 502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retries))

    try:
        response = session.get(url, headers=headers, timeout=30)
        response.raise_for_status()  # Raise error for bad responses (4xx, 5xx)

        # Parse JSON response
        data = json.loads(response.text)

        # Extract subdomains
        subdomains = {entry["name_value"].replace("*.","") for entry in data}

        # Save to file (no terminal output)
        with open(output_file, "w", buffering=1) as file:
            for subdomain in sorted(subdomains):
                file.write(subdomain + "\n")  # Write only to file (no print)

        print(f"Subdomains saved to {output_file}")  # Only print this message

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find subdomains using crt.sh")
    parser.add_argument("domain", help="The target domain to search for subdomains")
    parser.add_argument("-o", "--output", help="Output file name (default: output.txt)", default="output.txt")
    args = parser.parse_args()

    find_subdomains(args.domain, args.output)
