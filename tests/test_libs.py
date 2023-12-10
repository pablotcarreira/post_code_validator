from unittest import mock
from unittest.mock import AsyncMock, patch

import aiohttp
import pytest

from libs.uk_post_code_cache import FetchPostCodesError, load_post_codes_from_online_provider
from libs.uk_post_code_cache import load_fallback_postcodes
from libs.uk_post_code_validator import validate_post_code


class TestValidatePostCode:

    @pytest.fixture(autouse=True)
    def set_up(self):
        self.post_code_cache = set()

    def test_valid_post_code_strict_true(self):
        self.post_code_cache.add('EC1A 1BB')
        result = validate_post_code('EC1A1BB', True, self.post_code_cache)
        assert result == 'EC1A 1BB'
        result = validate_post_code('EC1A1BC', True, self.post_code_cache)
        assert result is False

    def test_valid_post_code_strict_false(self):
        result = validate_post_code('EC1A1BC', False, self.post_code_cache)
        assert result == 'EC1A 1BC'

    def test_invalid_post_code_strict_true(self):
        result = validate_post_code('INVALID', True, self.post_code_cache)
        assert result is False

    def test_invalid_post_code_strict_false(self):
        result = validate_post_code('INVALID', False, self.post_code_cache)
        assert result is False


@pytest.mark.asyncio
async def test_load_fallback_postcodes():
    with patch('libs.uk_post_code_cache.aiofiles.open') as mock_open:
        fake_content = ['123\n', '456\n', '789\n']
        mock_file = AsyncMock()
        mock_file.__aenter__.return_value.readlines.return_value = fake_content
        mock_open.return_value = mock_file
        postcodes = await load_fallback_postcodes('fake_file.txt')
        assert postcodes == {'123', '456', '789'}


