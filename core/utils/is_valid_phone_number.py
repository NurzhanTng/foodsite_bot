import re


def is_valid_phone_number(phone_number: str):
    # Regular expression pattern
    pattern = r'^\+?(7|8)7([0124567][0-8]\d{7})$'

    # Check if the string matches the pattern
    if re.match(pattern, phone_number):
        return True
    else:
        return False
