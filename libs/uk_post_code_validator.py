import re

clean_post_code = re.compile('[^A-Za-z0-9]+')

# Thank you wikipedia!
validate_post_code_regex = re.compile(
    '^(([A-Z]{1,2}[0-9][A-Z0-9]?|ASCN|STHL|TDCU|BBND|[BFS]IQQ|PCRN|TKCA) ?[0-9][A-Z]{2}|BFPO ?[0-9]{1,4}|(KY[0-9]|MSR|VG|AI)[ -]?[0-9]{4}|[A-Z]{2} ?[0-9]{2}|GE ?CX|GIR ?0A{2}|SAN ?TA1)$')


def validate_post_code(post_code: str, strict_mode: bool, post_code_cache: set | None = None) -> str | bool:
    """Clean, format and validate a post. Returns the formatted post code if it is valid, otherwise returns False.
    If not on strict mode, check if the post code composition is valid.
    If on strict mode, the post code must exist in the cache. A set of well formatted post codes must be provided as cache in order to use strict mode.

    :param post_code: The post code to validate.
    :param strict_mode: Whether to use strict mode.
    :param post_code_cache: A cache containing acceptable post codes.
    """
    post_code = clean_post_code.sub('', post_code)
    post_code = post_code[:-3] + ' ' + post_code[-3:]
    if strict_mode:
        if post_code in post_code_cache:
            return post_code
    elif validate_post_code_regex.match(post_code):
        return post_code
    return False
