import os
import json
import subprocess
import sys

def main():
    api_key = os.environ.get("FANART_API_KEY")
    if not api_key:
        print("Warning: FANART_API_KEY environment variable is not set.")
        print("The script will proceed, but if it tries to download logos, it will fail without a key.")

    logos_json_path = os.path.join("KnowYourBand", "wwwroot", "data", "logos.json")
    base_root_dir = os.path.join("KnowYourBand", "wwwroot")

    if not os.path.exists(logos_json_path):
        print(f"Error: Could not find {logos_json_path}")
        sys.exit(1)

    with open(logos_json_path, "r") as f:
        try:
            bands = json.load(f)
        except json.JSONDecodeError:
            print(f"Error: {logos_json_path} is not valid JSON")
            sys.exit(1)

    missing_count = 0

    for band_data in bands:
        band_name = band_data.get("name")
        expected_logo_path = band_data.get("logo")

        if not band_name or not expected_logo_path:
            continue

        full_logo_path = os.path.join(base_root_dir, expected_logo_path)

        if not os.path.exists(full_logo_path):
            missing_count += 1
            print(f"Missing logo for {band_name}: {expected_logo_path}")

            if api_key:
                # The output directory should be the parent directory of the expected logo path
                out_dir = os.path.dirname(full_logo_path)

                print(f"Attempting to download logo for {band_name} to {out_dir}...")

                cmd = [
                    sys.executable,
                    "scripts/download_logo.py",
                    band_name,
                    "--api-key",
                    api_key,
                    "--out-dir",
                    out_dir
                ]

                try:
                    subprocess.run(cmd, check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Error running download script for {band_name}: {e}")
            else:
                print(f"Skipping download for {band_name} because FANART_API_KEY is not set.")

    if missing_count == 0:
        print("All logos are present!")
    else:
        print(f"Found {missing_count} missing logos.")

if __name__ == "__main__":
    main()
