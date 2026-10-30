import os
import requests
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def get_gps_info(exif_data):
    gps_info = {}
    for id, value in exif_data.items():
        tag = TAGS.get(id)
        if tag == "GPSInfo":
            for gps_id in value:
                gps_tag = GPSTAGS.get(gps_id, gps_id)
                gps_info[gps_tag] = value[gps_id]
    return gps_info

def convert_to_degrees(value):
    d = float(value[0])
    m = float(value[1])
    s = float(value[2])
    return d + (m / 60.0) + (s / 3600.0)

def extract_image_metadata(file_path):
    try:
        with Image.open(file_path) as img:
            exif = img._getexif()
            if not exif:
                print("[-] No EXIF metadata found in this image.")
                return

            exif_data = {}
            for tag_id, value in exif.items():
                tag = TAGS.get(tag_id, tag_id)
                exif_data[tag] = value

            print(f"\n[*] General Metadata:")
            fields = ["Make", "Model", "DateTime", "Software", "Artist", "Copyright"]
            for field in fields:
                if field in exif_data:
                    print(f"   [+] {field}: {exif_data[field]}")

            gps_data = get_gps_info(exif)
            if gps_data:
                print(f"\n[*] Geolocation Metadata (GPS):")
                try:
                    lat_value = gps_data.get("GPSLatitude")
                    lat_ref = gps_data.get("GPSLatitudeRef")
                    lon_value = gps_data.get("GPSLongitude")
                    lon_ref = gps_data.get("GPSLongitudeRef")

                    if lat_value and lat_ref and lon_value and lon_ref:
                        lat = convert_to_degrees(lat_value)
                        if lat_ref != "N":
                            lat = -lat

                        lon = convert_to_degrees(lon_value)
                        if lon_ref != "E":
                            lon = -lon

                        print(f"   [+] Latitude: {lat}")
                        print(f"   [+] Longitude: {lon}")
                        print(f"   [+] Google Maps Link: https://google.com{lat},{lon}")
                except Exception as gps_err:
                    print(f"   [-] Error parsing GPS data: {gps_err}")
            else:
                print("\n[-] No GPS geolocation coordinates found in metadata.")

    except Exception as e:
        print(f"[!] Error reading image file: {e}")

def metadataanalyzer():
    source = input("Enter local file path or URL: ").strip()
    if not source:
        return

    temp_file = "temp_analysis_target"
    is_downloaded = False

    if source.startswith("http://") or source.startswith("https://"):
        print("[*] Target is a URL. Downloading file for analysis...")
        try:
            response = requests.get(source, timeout=10)
            if response.status_code == 200:
                with open(temp_file, "wb") as f:
                    f.write(response.content)
                target_path = temp_file
                is_downloaded = True
            else:
                print(f"[!] Failed to download file. Status code: {response.status_code}")
                return
        except Exception as download_err:
            print(f"[!] Network error during download: {download_err}")
            return
    else:
        target_path = source

    if not os.path.exists(target_path):
        print(f"[!] Error: File '{target_path}' not found.")
        return

    print(f"\n[*] Target File: {source}")
    extract_image_metadata(target_path)

    if is_downloaded and os.path.exists(temp_file):
        os.remove(temp_file)

    print("\n[!] Analysis process finished.")
    input("Press Enter to exit...")

if __name__ == "__main__":
    metadataanalyzer()
