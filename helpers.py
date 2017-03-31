import argparse
import string
from sys import maxunicode
from unicodedata import category

version_number = '0.2.2'


class CapitalisedHelpFormatter(argparse.RawTextHelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = 'Usage: '
        return super(CapitalisedHelpFormatter, self).add_usage(
            usage, actions, groups, prefix)


arg_parser = argparse.ArgumentParser(description="""         _                               
 ___ _ _| |_ ___ ___ ___ ___ ___ _ _ ___ 
| . | | | . | . |  _| . | -_| . | | |_ -|
|  _|_  |___|___|_| |_  |___|___|___|___|
|_| |___|           |___|              

pyborgeous is an open-source implementation of Jorge Luis Borges' Library of Babel.
This library can utilize all printable Unicode characters.""",
                                     formatter_class=CapitalisedHelpFormatter,
                                     add_help=False,
                                     prog="pyborgeous",
                                     epilog="Check http://github.com/Spacehug/pyborgeous for updates")

# Capitalization of protected stuff
arg_parser._positionals.title = 'Positional arguments'  # I know this is bad
arg_parser._optionals.title = 'Optional arguments'  # Tell me if you know a better way, please

# Optional arguments
arg_parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS, help="""
Show this help message and exit
Usage: pyborgeous -h

""")
arg_parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {version_number}", help="""
Show program version number and exit
Usage: pyborgeous -v

""")
arg_parser.add_argument("-t", "--test", action="store_true", dest="test", help="""
Test the current development operation behavior
Returns result from "if __name__ == '__main__' and args.test:" block.

""")
arg_parser.add_argument("-d", "--dump", dest="file", help="""
Dump the result to specified file
Default: 'result.txt'
Usage: pyborgeous -d 'result.txt'

""")

# Mutually exclusive arguments groups (m, n)
arg_mgroup = arg_parser.add_mutually_exclusive_group(required=True)
arg_mgroup.add_argument("-m", "--mode", dest="mode", help="""
Build the library in given mode
Usage: pyborgeous -m borges
Choices: binary, morse, borges, classic, full, unicode
If you want to use custom charset, use -c 'abcde' or -cf 'charset.txt'

""")
arg_mgroup.add_argument("-c", "--charset", dest="charset", help="""
Build the library using custom charset
Usage: pyborgeous -c '0123456789ABCDEF'
Warning: don't use \\t (ASCII TAB) control character, or there will be trouble.

""")
arg_mgroup.add_argument("-cf", "--charset-file", dest="charset_file", help="""
Build the library using custom charset from a file
Usage: pyborgeous -cf 'charset.txt'
Warning: don't use \\t (ASCII TAB) control character in your file, or there will be trouble.

""")

arg_ngroup = arg_parser.add_mutually_exclusive_group(required=True)
arg_ngroup.add_argument("-p", "--page-address", dest="address", help="""
Find a page by address
Usage: pyborgeous -p <LONG ADDRESS>

""")
arg_ngroup.add_argument("-af", "--address-file", dest="address_file", help="""
Find a page by address from a file
Format should be: room\\tbookcase[1-4]\\tshelf[1-5]\\tbook[1-32]\\tpage_number[1-410]
\\t is ASCII TAB control character, not literal \\t
Usage: pyborgeous -af 'address.txt'

""")
arg_ngroup.add_argument("-s", "--search", dest="search_text", help="""
Find a page that contains only the text given and nothing else
Usage: pyborgeous -s 'The first colony on Mars was founded in 2031'
Note: Text longer than 3200 symbols will be truncated

""")
arg_ngroup.add_argument("-sr", "--search-random", dest="search_text_random", help="""
Find a page that contains the text given, along with random words/symbols
Usage: pyborgeous -sr 'The first colony on Mars was founded in 2031'
Note: Text longer than 3200 symbols will be truncated

""")
arg_ngroup.add_argument("-sf", "--search-file", dest="text_file", help="""
Find a page that contains only the text from a file and nothing else
Usage: pyborgeous -sf text.txt
Note: Text longer than 3200 symbols will be truncated

""")


command_line = arg_parser.parse_args()


def generate_unicode_string(mode):
    if mode == 'regular':
        skip_cats = ('Cc', 'Cf', 'Cs', 'Co', 'Cn',
                     'Zl', 'Zp')
    elif mode == 'address':
        skip_cats = ('Cc', 'Cf', 'Cs', 'Co', 'Cn',
                     'Zl', 'Zs', 'Zp',
                     'Mn', 'Mc', 'Me',
                     'Pc', 'Pd', 'Ps', 'Pe', 'Pi', 'Pf', 'Po',
                     'Sm', 'Sc', 'Sk', 'So')
    return ''.join(filter(lambda x: category(x) not in skip_cats, map(chr, range(maxunicode))))


def base_to_int(basenumber, basestring):
    integer = 0
    for digit in str(basenumber):
        integer = integer * len(basestring) + basestring.index(digit)
    return integer


def int_to_base(number, basestring):
    digits = []
    base = len(basestring)
    while number:
        digits.append(basestring[number % base])
        number //= base
    digits.reverse()
    return ''.join(digits)


def string_to_int(text):
    new = bytes(text, 'utf-8')
    return int.from_bytes(new, byteorder='little')


def int_to_string(number):
    text = number.to_bytes((number.bit_length() + 7) // 8, byteorder='little')
    return text.decode("utf-8")


def get_address():
    if command_line.address_file:
        current_address = DataFile(command_line.address_file)
        current_address.load()
        return current_address.data
    elif command_line.address:
        return command_line.address
    else:
        return None


def get_text():
    if command_line.search_text:
        return command_line.search_text
    elif command_line.search_text_random:
        return command_line.search_text_random
    elif command_line.text_file:
        current_text = DataFile(command_line.search_file)
        return current_text.load()
    else:
        return None


def get_encode_string():
    if command_line.mode:
        if command_line.mode == 'binary':
            return '01'
        elif command_line.mode == 'morse':
            return '-. '
        elif command_line.mode == 'borges':
            return 'abcdefghijlmnoprstuvyz, .'
        elif command_line.mode == 'classic':
            return string.ascii_lowercase + ', .'
        elif command_line.mode == 'full':
            return string.digits + string.ascii_letters + ' ' + string.punctuation
        elif command_line.mode == 'unicode':
            return generate_unicode_string('regular')
        else:
            raise NotImplementedError("This mode is not implemented yet.")
    elif command_line.charset:
        return command_line.charset
    elif command_line.charset_file:
        charset_string = DataFile(command_line.charset_file)
        charset_string.load()
        return charset_string.data
    else:
        raise NotImplementedError("I don't really know how did you get this.")


class DataFile:

    def __init__(self, file_name, *data):
        self.file_name = file_name
        self.data = data

    def load(self):
        with open(self.file_name, 'r', encoding='utf-8') as input_file:
            self.data = input_file.read()

    def save(self):
        with open(self.file_name, 'w', encoding='utf-8') as output_file:
            output_file.writelines(self.data)
