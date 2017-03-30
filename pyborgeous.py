# Open-source implementation of Jorge Luis Borges' Library of Babel that utilizes all printable Unicode characters
# Started 2017/03/27
# TODO: MAIN LOGIC
# TODO: PAGE GENERATION BY ADDRESS
# TODO: ADDRESS GENERATION BY PAGE
# TODO: TODOs


import argparse
# import random
import sys
import string
from unicodedata import category


# TODO: Refactor to a class in separate file
version_number = '0.1.1'


class CapitalisedHelpFormatter(argparse.RawTextHelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = 'Usage: '
        return super(CapitalisedHelpFormatter, self).add_usage(
            usage, actions, groups, prefix)

# TODO: Mark which are done and which are not
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

# Capitalization of protected stuff DONE
arg_parser._positionals.title = 'Positional arguments'  # I know this is bad
arg_parser._optionals.title = 'Optional arguments'      # Tell me if you know a better way, please

# Optional arguments DONE
arg_parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS, help="""
Show this help message and exit
Usage: pyborgeous -h

""")
arg_parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {version_number}", help="""
Show program version number and exit
Usage: pyborgeous -v

""")
# TODO: assign dump filename to specified here, need completed logic to utilize these
arg_parser.add_argument("-d", "--dump", dest="file", default="result.txt", help="""
Dump the result to specified file
Default: 'result.txt'
Usage: pyborgeous -d 'test.txt'

""")

# Mutually exclusive arguments group
arg_mgroup = arg_parser.add_mutually_exclusive_group(required=True)
# TODO: add ModeSelector class that uses one of these modes if a mode is specified, otherwise load -c or -cf
arg_mgroup.add_argument("-m", "--mode", dest="mode", help="""
Build the library in given mode
Usage: pyborgeous -m borges
Choices: binary, morse, borges, classic, unicode
If you want to use custom charset, use -c 'abcde' or -cf 'charset.txt'

""")
arg_mgroup.add_argument("-c", "--charset", dest="charset", help="""
Build the library using given charset
Usage: pyborgeous -c '0123456789ABCDEF'

""")
arg_mgroup.add_argument("-cf", "--charset-file", dest="charset_file", help="""
Build the library using given charset from a file
Usage: pyborgeous -cf 'charset.txt'

""")

arg_ngroup = arg_parser.add_mutually_exclusive_group(required=True)
# TODO: Need complete logic to utilize these
arg_ngroup.add_argument("-p", "--page-address", dest="address", help="""
Find a page by address
Usage: pyborgeous -p <LONG ADDRESS>

""")
arg_ngroup.add_argument("-af", "--address-file", dest="address_file", help="""
Find a page by address from a file
Usage: pyborgeous -af 'address.txt'

""")
arg_ngroup.add_argument("-s", "--search", dest="search_text", help="""
Find a page that contains only the text given and nothing else
Usage: pyborgeous -s 'The first colony on Mars was founded in 2031'

""")
arg_ngroup.add_argument("-sr", "--search-random", dest="search_text", help="""
Find a page that contains the text given, along with random words/symbols
Usage: pyborgeous -sr 'The first colony on Mars was founded in 2031'

""")
arg_ngroup.add_argument("-st", "--search-title", dest="search_title", help="""
Find a title that contains the given text
Only the first 25 characters will be processed
Usage: pyborgeous -st 'The first Martian colony'

""")
arg_ngroup.add_argument("-sf", "--search-file", dest="text_file", help="""
Find a page that contains only the text from a file and nothing else
Usage: pyborgeous -sf text.txt

""")
arg_ngroup.add_argument("-t", "--test", action="store_true", dest="test", help="""
Test the current development operation behavior
Returns result from "if __name__ == '__main__' and args.test:" block.

""")

command_line = arg_parser.parse_args()


def generate_unicode_string():
    skip_cats = ('Cc', 'Cf', 'Cs', 'Co', 'Cn', 'Zl', 'Zp')
    return ''.join(filter(lambda x: category(x) not in skip_cats, map(chr, range(sys.maxunicode))))


def int_to_base(number, basestring):
    digits = []
    base = len(basestring)
    while number:
        digits.append(basestring[number % base])
        number //= base
    digits.reverse()
    return ''.join(digits)


def text_to_number(text):
    new = bytes(text, 'utf-8')
    return int.from_bytes(new, byteorder='little')


def number_to_text(number):
    text = number.to_bytes((number.bit_length() + 7) // 8, byteorder='little')
    return text.decode("utf-8")


def get_encode_string(mode, charset, charset_file):
    if mode:
        if mode == 'binary':
            return '01'
        elif mode == 'morse':
            return '-. '
        elif mode == 'borges':
            return 'abcdefghijlmnoprstuvyz, .'
        elif mode == 'classic':
            return string.ascii_letters + ', .'
        elif mode == 'unicode':
            return generate_unicode_string()
        else:
            raise NotImplementedError("This mode is not implemented yet.")
    elif charset:
        return charset
    elif charset_file:
        charset_string = DataFile(charset_file)
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
            output_file.write(self.data)


if __name__ == '__main__' and command_line.test:
    pass
