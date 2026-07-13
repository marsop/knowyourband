import requests
import os
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description="Download transparent band logos from Fanart.tv for a specific band."
    )
    parser.add_argument(
        "band",
        help="Band name to download logos for. Quote names with spaces.",
    )
    parser.add_argument(
        "--api-key",
        required=True,
        help="Fanart.tv API Key.",
    )
    parser.add_argument(
        "--out-dir",
        required=True,
        help="Directory to save the logos.",
    )

    return parser.parse_args()

def get_artist_mbid(band_name):
    """Finds the MusicBrainz ID for a given band name."""
    url = f"https://musicbrainz.org/ws/2/artist/?query=artist:{band_name}&fmt=json"
    headers = {"User-Agent": "BandLogoDownloader/1.0 ( your_email@example.com )"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data.get("artists"):
            # Return the first/best match
            return data["artists"][0]["id"], data["artists"][0]["name"]
    print(f"❌ Could not find an ID for '{band_name}' on MusicBrainz.")
    return None, None

def download_band_logos(mbid, clean_name, api_key, save_dir):
    """Fetches ONLY transparent band logos from Fanart.tv."""
    url = f"https://webservice.fanart.tv/v3.2/music/{mbid}"
    headers = {"api-key": api_key}

    response = requests.get(url, headers=headers)
    if response.status_code == 404:
        print(f"❌ No artwork profiles exist on Fanart.tv for {clean_name}.")
        return
    elif response.status_code != 200:
        print(f"❌ Fanart.tv API Error: Status {response.status_code}")
        return

    data = response.json()
    os.makedirs(save_dir, exist_ok=True)

    # We strictly target logo keys, ignoring 'albums', 'artistbackground', etc.
    logo_keys = ["hdmusiclogo", "musiclogo"]
    found_logo = False

    # Track overall index for naming across keys
    overall_idx = 0
    base_name = clean_name.lower().replace(' ', '')

    for key in logo_keys:
        if key in data:
            found_logo = True
            print(f"Found {len(data[key])} graphics under '{key}'...")
            for logo_item in data[key]:
                logo_url = logo_item["url"]

                # Fetching the raw image
                img_data = requests.get(logo_url).content

                if overall_idx == 0:
                    file_name = f"{base_name}.png"
                else:
                    file_name = f"{base_name}_{overall_idx}.png"

                file_path = os.path.join(save_dir, file_name)

                with open(file_path, "wb") as f:
                    f.write(img_data)
                print(f"💾 Saved: {file_path}")
                overall_idx += 1

    if not found_logo:
        print(f"ℹ️ {clean_name} has a profile, but no transparent text logos were uploaded there yet.")

# Run the process
if __name__ == "__main__":
    args = parse_args()

    print(f"Searching for '{args.band}'...")
    mbid, clean_name = get_artist_mbid(args.band)

    if mbid:
        print(f"🔗 Match found: {clean_name} (MBID: {mbid})")
        download_band_logos(mbid, args.band, args.api_key, args.out_dir)
