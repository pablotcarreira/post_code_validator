import logging

import pytest
from unittest import mock
from libs.app_init import get_logger, load_post_codes_cache


# Create a mock Logger instance
mock_logger = mock.MagicMock(spec=logging.Logger)


@pytest.mark.asyncio
async def test_load_post_codes_cache_online():
    with mock.patch('libs.app_init.load_post_codes_from_online_provider', return_value={"AA1", "BB2", "CC3"}):
        post_code_cache = await load_post_codes_cache(
            "https://api.test.com/downloads/v1/products/CodePointOpen/downloads?area=GB&format=CSV&redirect",
            "./Data/CSV",
            "libs/post_codes.txt",
            mock_logger,
            allow_fallback=True
        )
    mock_logger.info.assert_called_with("Post codes cache loaded successfully with 3 entries.")
    assert len(post_code_cache) == 3


@pytest.mark.asyncio
async def test_load_post_codes_cache_fallback():
    with mock.patch('libs.app_init.load_post_codes_from_online_provider', side_effect=Exception), \
            mock.patch('libs.app_init.load_fallback_postcodes', return_value={"DD4", "EE5", "FF6"}):
        post_code_cache = await load_post_codes_cache(
            "https://api.test.com/downloads/v1/products/CodePointOpen/downloads?area=GB&format=CSV&redirect",
            "./Data/CSV",
            "libs/post_codes.txt",
            mock_logger,
            allow_fallback=True
        )
    # Assert fallback was used.
    mock_logger.error.assert_called_with("Can't load post cods from online provider (https://api.test.com/downloads/v1/products/CodePointOpen/downloads?area=GB&format=CSV&redirect), falling back to local post codes.")
    mock_logger.info.assert_called_with("Post codes cache loaded successfully with 3 entries.")
    assert len(post_code_cache) == 3
