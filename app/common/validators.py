from .helpers import is_valid_email


def email(email_str):
    """Return email_str if valid, raise an exception in other case."""
    if is_valid_email(email_str):
        return email_str
    else:
        raise ValueError('{} is not a valid email'.format(email_str))
