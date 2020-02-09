import re


EMAIL_RFC5322 = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


def is_valid_email(candidate):
    """
    Validates an email address using RFC5322
    Courtesy of: https://emailregex.com/
    """
    return EMAIL_RFC5322.match(candidate)
