import phonenumbers
import os

with open('numbers.txt', 'r') as infile:
    for number in infile:
        try:
            n = phonenumbers.parse(number, 'SE')
        except (phonenumbers.phonenumberutil.NumberParseException,
                UnicodeDecodeError):
            continue
        if phonenumbers.number_type(n) == phonenumbers.PhoneNumberType.MOBILE:
            print(phonenumbers.format_number(n,
                                             phonenumbers.PhoneNumberFormat.E164))

