import logging

from libs.uk_post_code_cache import load_post_codes_from_online_provider, load_fallback_postcodes, FetchPostCodesError


def get_logger():
    """Set up the logger."""
    logger = logging.getLogger("post_code_validator")
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


async def load_post_codes_cache(url, csv_folder, local_file, logger: logging.Logger, allow_fallback=True) -> set:
    """Populate the post code cache.
        - First try to load fresh data from Code Point Open or any other zip+csv provider.
        - If it fails and allow fallback is True, load the fallback post codes.


    :param url: URL to fetch post codes from.
    :param csv_folder: Path to the csv folder where the post codes will be.
    :param local_file: Path to a local fallback file.
    :param allow_fallback: Load the fallback post codes in case of failure.
    :param logger: A logger instance.
    """
    logger.info("Loading post codes cache...")
    try:
        cache = await load_post_codes_from_online_provider(url, csv_folder)
    except:
        if allow_fallback:
            logger.error(f"Can't load post cods from online provider ({url}), falling back to local post codes.")
            cache = await load_fallback_postcodes(local_file)
        else:
            logger.error(f"Can't load post codes.", exc_info=True)
            raise FetchPostCodesError(f"Can't load post codes.")

    logger.info(f"Post codes cache loaded successfully with {len(cache)} entries.")
    return cache
