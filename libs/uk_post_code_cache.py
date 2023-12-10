import aiohttp
import aiofiles
import zipfile
import os
import glob
import pandas as pd
import tempfile

from aiohttp import ClientConnectorError


class FetchPostCodesError(Exception):
    def __init__(self, message):
        self.message = message


async def load_fallback_postcodes(file: str) -> set:
    """Load postcodes from the fallback file."""
    async with aiofiles.open(file, mode='r') as f:
        postcodes = {line.strip() for line in await f.readlines()}
    return postcodes


async def _read_post_codes_pack(data: bytes, csv_folder: str) -> set:
    """Read postcodes from a ziped postcodes file."""
    with tempfile.TemporaryDirectory() as temp_dir:
        output = os.path.join(temp_dir, "file.zip")

        async with aiofiles.open(output, 'wb') as out_file:
            await out_file.write(data)

        with zipfile.ZipFile(output, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        csv_folder = os.path.join(csv_folder, "*.csv")
        path = os.path.join(temp_dir, csv_folder)
        post_codes = set()
        for fname in glob.glob(path):
            df = pd.read_csv(fname, header=None)
            post_codes.update(df[0].values)

    return post_codes


async def load_post_codes_from_online_provider(url: str, csv_folder: str) -> set:
    """Fetch post codes from an online provider, e.g Code-Point Open, and return a set of valid post codes.
    Could be any provider of a zip+csv file where the first column contains postcodes.

    :param url: Download URL.
    :param csv_folder: Path to the folder inside the zipfile containing one or more csv files.
    :return: A set of post codes.
    """
    session = aiohttp.ClientSession()

    try:
        response = await session.get(url)
    except ClientConnectorError:
        await session.close()
        raise FetchPostCodesError("Can't connect to provider.")
    except AssertionError:
        await session.close()
        raise FetchPostCodesError("Bad URL.")

    if response.status != 200:
        raise FetchPostCodesError(f"Failed to download file - status code: {response.status}.")

    try:
        data = await response.content.read()
    except:
        await session.close()
        raise FetchPostCodesError("Failed to download file content.")
    else:
        await session.close()

    return await _read_post_codes_pack(data, csv_folder)
