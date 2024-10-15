# Load standard library
import sys
from pathlib import Path
import argparse
import requests
from datetime import datetime
import gzip
import re

# Set path and name
py_folder_path = Path(__file__).parent


def parse_and_validate_arguments():
    print(f"function: {sys._getframe().f_code.co_name}")
    # Parse arguments
    parser = argparse.ArgumentParser(description="Type the architecture name")
    parser.add_argument(
        "architecture",
        help="Architecture list (amd64, arm64, armel, armhf, i386, mips64el, "
        "mipsel, ppc64el, s390x)",
    )
    args = parser.parse_args()
    # Validate user input with list
    arch_list = [
        "arm65",
        "amd64",
        "arm64",
        "armel",
        "armhf",
        "i386",
        "mips64el",
        "mipsel",
        "ppc64el",
        "s390x",
    ]
    arch_name = args.architecture
    if arch_name not in arch_list:
        print(f"Invalid architecture name: {arch_name}")
        print(f"Supported architectures: {arch_list}")
        exit(1)
    return arch_name


def download_file(download_url, download_folder_path, file_name):
    # Download the file
    print(f"function: {sys._getframe().f_code.co_name}")
    response = requests.get(download_url, timeout=10)
    response.raise_for_status()
    if response.status_code == 200:
        local_file_path = f"{download_folder_path}/{file_name}.gz"
        with open(local_file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)
        print(f"Downloaded file: {local_file_path}")
        return local_file_path
    else:
        response.raise_for_status()
        exit(1)


def check_content_file(download_url, download_folder_path, file_name):
    # Check if the file need to be updated
    print(f"function: {sys._getframe().f_code.co_name}")
    file_need_updated = False
    Path(download_folder_path).mkdir(exist_ok=True)
    local_file_path = f"{download_folder_path}/{file_name}.gz"
    if Path(local_file_path).exists():
        # Get url file info to check if the file is updated
        response = requests.head(download_url, timeout=10)
        if response.status_code == 200:
            url_modified_date = response.headers.get("last-modified")
            dt_obj = datetime.strptime(url_modified_date, "%a, %d %b %Y %H:%M:%S GMT")
            url_modified_timestamp = datetime.timestamp(dt_obj)
        else:
            print("Failed to get the file info from the server")
            exit(1)
        # Get local file info
        local_file = Path(local_file_path)
        local_modified_timestamp = local_file.stat().st_mtime
        if local_modified_timestamp < url_modified_timestamp:
            file_need_updated = True
        else:
            file_need_updated = False
    else:
        file_need_updated = True
    return file_need_updated


def analyze_file(contents_file_path):
    # Analyze the file
    print(f"function: {sys._getframe().f_code.co_name}")
    package_dict = {}
    with gzip.open(contents_file_path, "rt") as file:
        for line in file:
            line_info = line.strip()
            line_info = re.sub(" +", " ", line_info)
            package_name_str = line_info.split(" ")[-1]
            package_name_list = re.findall(r"[^,\s]+", package_name_str)
            for package_name in package_name_list:
                package_name = package_name.split("/")[1]
                package_dict[package_name] = package_dict.get(package_name, 0) + 1
    sorted_list = sorted(package_dict.items(), key=lambda item: item[1], reverse=True)
    top_10_list = sorted_list[:10]
    package_dict = dict(top_10_list)
    print(f"Analyzed file: {contents_file_path}")
    return package_dict


def main():
    print(f"function: {sys._getframe().f_code.co_name}")
    # Parse architecture from arguments
    arch_name = parse_and_validate_arguments()
    # Check content-*.gz file need to be updated or not
    file_name = f"Contents-{arch_name}"
    download_url = f"http://ftp.uk.debian.org/debian/dists/stable/main/{file_name}.gz"
    download_folder_path = f"{py_folder_path}/download"
    file_need_updated = check_content_file(download_url, download_folder_path, file_name)
    # Download the file
    if file_need_updated:
        contents_file_path = download_file(download_url, download_folder_path, file_name)
    else:
        contents_file_path = f"{download_folder_path}/{file_name}.gz"
    # Analyze the file
    package_dict = analyze_file(contents_file_path)
    # Report the statistics
    print(f"Top 10 packages in {arch_name} architecture\nPackage Name: Number of files")
    for key, value in package_dict.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    # Start main
    main()
