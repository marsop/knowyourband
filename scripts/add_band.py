import argparse
import json
import os
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser(description="Add a new band to logos.json and download its logo.")
    parser.add_argument("band", help="The name of the band to add.")
    args = parser.parse_args()

    band_name = args.band
    clean_name = band_name.lower().replace(' ', '')
    logo_path = f"images/logos/{band_name}/{clean_name}.png"

    logos_json_path = os.path.join("KnowYourBand", "wwwroot", "data", "logos.json")

    if not os.path.exists(logos_json_path):
        print(f"Error: Could not find {logos_json_path}")
        sys.exit(1)

    with open(logos_json_path, "r") as f:
        try:
            bands = json.load(f)
        except json.JSONDecodeError:
            print(f"Error: {logos_json_path} is not valid JSON")
            sys.exit(1)

    # Check if band already exists
    for band in bands:
        if band.get("name", "").lower() == band_name.lower():
            print(f"Band '{band_name}' already exists in {logos_json_path}.")
            sys.exit(0)

    # Add band
    new_band = {
        "name": band_name,
        "logo": logo_path
    }
    bands.append(new_band)

    with open(logos_json_path, "w") as f:
        json.dump(bands, f, indent=4)

    print(f"Added '{band_name}' to {logos_json_path}.")

    # Run get_missing_logos.py to fetch the logo
    print("Running get_missing_logos.py to fetch the newly added logo...")
    cmd = [sys.executable, "scripts/get_missing_logos.py"]
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running get_missing_logos.py: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
