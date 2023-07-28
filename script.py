import os
import logging
import functools
import requests
import xmltodict

DIR_URL = "https://msedgewebdriverstorage.blob.core.windows.net"
DOWNLOAD_URL = "https://msedgedriver.azureedge.net/"
FILE_NAME = "edgedriver_win64.zip"
CHUNK_SIZE = 32 * 1024

# Configure logging to a file
logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def optional_index(a, i):
    if i > len(a) - 1:
        return 0
    return a[i]


def compare_driver_version(v1, v2):
    v1_tokens = list(map(lambda s: int(s), v1.split(".")))
    v2_tokens = list(map(lambda s: int(s), v2.split(".")))
    max_len = max(len(v1_tokens), len(v2_tokens))
    for token_index in range(max_len):
        if optional_index(v1_tokens, token_index) < optional_index(
            v2_tokens, token_index
        ):
            return -1
        elif optional_index(v1_tokens, token_index) > optional_index(
            v2_tokens, token_index
        ):
            return 1
        elif token_index == max_len - 1:
            return 0
        else:
            continue


# Get versions from Selenium nested folders
def get_file_content_in_folder(folder_path):
    versions = []
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name != "version":
                continue
            file_path = os.path.join(root, file_name)
            with open(file_path, "r") as f:
                content = f.read()
                versions.append(content)
                logging.info(f"{file_path}: {content}")
    return versions


def get_newest_local_version(folder):
    versions = get_file_content_in_folder(folder)
    if len(versions) > 0:
        versions.sort(key=functools.cmp_to_key(compare_driver_version))
        return versions[-1]
    else:
        return "0"


def get_newest_remote_version(local_version):
    response = requests.get(
        f"{DIR_URL}/edgewebdriver?delimiter=%2F&maxresults=9999999&restype=container&comp=list&_=1690564408683&timeout=60000"
    )
    r_dict = xmltodict.parse(response.content)
    remote_versions = list(
        map(
            lambda v: v["Name"][:-1],
            r_dict["EnumerationResults"]["Blobs"]["BlobPrefix"],
        )
    )
    remote_versions.sort(key=functools.cmp_to_key(compare_driver_version))
    remote_newest = remote_versions[-1] if len(remote_versions) > 0 else "0"
    return remote_newest


def download_driver(version):
    newest_url = f"{DOWNLOAD_URL}/{version}/{FILE_NAME}"
    driver_major_ver = version.split(".")[0]
    new_dir_name = os.path.join(os.getcwd(), f"selenium/EdgeChromium{driver_major_ver}")
    try:
        os.mkdir(new_dir_name)
    except:
        pass
    local_filename = os.path.join(new_dir_name, f"{FILE_NAME}")
    response = requests.get(newest_url, params={"stream": True})
    if response.status_code == 200:
        with open(local_filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)
    logging.info(f"download to {local_filename} complete")
    with open(os.path.join(new_dir_name, "version"), "w") as f:
        f.write(version)


if __name__ == "__main__":
    local_newest = get_newest_local_version("./selenium")
    logging.info(f"newest local version detected: {local_newest}")
    remote_newest = get_newest_remote_version(local_newest)
    logging.info(f"newest remote version detected: {remote_newest}")
    version_compare = compare_driver_version(remote_newest, local_newest)
    if version_compare:
        logging.info("versions mismatch")
    if version_compare < 0:
        logging.info(
            f"local versions {local_newest} is newer that remote {remote_newest}, aborting"
        )
    elif version_compare > 0:
        download_driver(remote_newest)
    else:
        logging.info(f"there is no newer version to download")
