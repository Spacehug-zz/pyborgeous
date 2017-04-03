import argparse
import docstrings
import random
import string
from collections import namedtuple
from sys import maxunicode
from unicodedata import category

__VERSION__ = '0.2.7'


class Page:
    """
    The page in a book in a shelf in a bookcase in a room in a library object
    """

    Room = namedtuple('Room', 'PAGES_PER_BOOK BOOKS_PER_SHELF SHELVES_PER_BOOKCASE BOOKCASES_PER_ROOM')
    library_configuration = Room(410, 32, 5, 4)

    # We iterate trough library_configuration, that's why page_configuration is separated from it
    PageContainer = namedtuple('PageContainer', 'CHARACTERS_PER_PAGE CHARACTERS_PER_PAGE_TITLE')
    page_configuration = PageContainer(3200, 25)

    def __init__(self, encode_string, page_text, address):
        """
        Instantiates the object with encode string,
        and address if there is no page text provided
        or page text if there is no address provided
        """

        self.encode_string = encode_string
        self.address = address
        self.page_text = page_text

    def get_page_text_by_address(self):
        """
        Transforms coordinates back to page text
        [Base number, int, int, int, int] ~> int ~> string 
        """

        address = self.address.split('\t')
        magic_number = base_to_integer(address[0], self.encode_string)

        for config, address_item in zip(reversed(self.library_configuration), address[1:]):

            magic_number = magic_number * config + int(address_item)

        self.page_text = integer_to_text(magic_number)

        return self.page_text

    def get_address_by_page_text(self):
        """
        Fills the rest of page with spaces,
        then transforms it to magic number,
        and then to page coordinates using calculate_coordinates()
        """

        space = ' '

        # If text is shorter than 3200 characters, fill the rest with spaces
        if len(self.page_text) < self.page_configuration.CHARACTERS_PER_PAGE:
            self.page_text += space * (self.page_configuration.CHARACTERS_PER_PAGE - len(self.page_text))

        # If text is longer than 3200 characters, truncate it
        elif len(self.page_text) > self.page_configuration.CHARACTERS_PER_PAGE:
            self.page_text = self.page_text[:self.page_configuration.CHARACTERS_PER_PAGE + 1]

        self.address = self.calculate_coordinates()

        return self.address

    def get_address_by_page_text_random(self):
        """
        Fills the page with random characters before and after the given string,
        then transforms it to magic number,
        and then to page coordinates using calculate_coordinates()
        """

        # If text is shorter than 3200 characters, fill the rest with random characters on both sides
        if len(self.page_text) < self.page_configuration.CHARACTERS_PER_PAGE:
            postfix_range = random.randrange(self.page_configuration.CHARACTERS_PER_PAGE - len(self.page_text) - 1)
            prefix_range = self.page_configuration.CHARACTERS_PER_PAGE - len(self.page_text) - postfix_range
            prefix = ''.join(random.choice(self.encode_string) for _ in range(prefix_range))
            postfix = ''.join(random.choice(self.encode_string) for _ in range(postfix_range))
            self.page_text = prefix + self.page_text + postfix

        # If text is longer than 3200 characters, truncate it
        elif len(self.page_text) > self.page_configuration.CHARACTERS_PER_PAGE:
            self.page_text = self.page_text[:self.page_configuration.CHARACTERS_PER_PAGE + 1]

        self.address = self.calculate_coordinates()

        return self.address

    def calculate_coordinates(self):
        """
        Transforms page_text to page coordinates using ceil division
        string ~> int ~> [Base number, int, int, int, int] 
        Format of the resulting address is: encoded room \t bookcase \t shelf \t book \t page
        """

        address = []
        magic_number = text_to_integer(self.page_text)

        for value in self.library_configuration:
            result_value = magic_number % value
            address.append(str(result_value))
            magic_number = - ((magic_number - result_value) // - value)  # Faster than 'from math import ceil'

        address.append(integer_to_base(magic_number, self.encode_string))

        return '\t'.join(reversed(address))


class DataFile:
    """
    Input/Output file handler object
    """

    def __init__(self, file_name=None, data=None):
        self.file_name = file_name
        self.data = data

    def load(self):
        with open(self.file_name, 'r', encoding='utf-8') as input_file:
            self.data = input_file.read()

        return self.data

    def save(self):
        with open(self.file_name, 'w', encoding='utf-8') as output_file:
            output_file.writelines(self.data)
            print("Output saved in", self.file_name)


def main():
    """
    Main logic here
    Parses command line arguments then executes Page methods, prints the data and writes it to a file if specified
    """

    class CapitalisedHelpFormatter(argparse.RawTextHelpFormatter):
        """
        Cosmetics. Used to override 'usage: ' string to 'Usage: '
        """

        def add_usage(self, usage, actions, groups, prefix=None):

            if prefix is None:
                prefix = 'Usage: '

            return super(CapitalisedHelpFormatter, self).add_usage(usage, actions, groups, prefix)

    arg_parser = argparse.ArgumentParser(description=docstrings.PROGRAM_DESCRIPTION,
                                         formatter_class=CapitalisedHelpFormatter,
                                         add_help=False,
                                         prog="pyborgeous",
                                         epilog=docstrings.PROGRAM_EPILOG)

    # Capitalization of protected stuff
    arg_parser._positionals.title = 'Positional arguments'  # I know this is bad
    arg_parser._optionals.title = 'Optional arguments'      # Tell me if you know a better way, please

    # Optional arguments
    arg_parser.add_argument("-h", "--help", action="help",
                            default=argparse.SUPPRESS, help=docstrings.HELP_HELP)
    arg_parser.add_argument("-v", "--version", action="version",
                            version="%(prog)s {0}".format(__VERSION__), help=docstrings.HELP_VERSION)
    arg_parser.add_argument("-o", "--output",
                            dest="output_file", help=docstrings.HELP_OUTPUT)

    # Mutually exclusive arguments group for charset
    arg_charset = arg_parser.add_mutually_exclusive_group(required=True)
    arg_charset.add_argument("-c", "--charset",
                             dest="charset", help=docstrings.HELP_CHARSET)
    arg_charset.add_argument("-cm", "--charset-mode",
                             dest="charset_mode", help=docstrings.HELP_CHARSET_MODE)
    arg_charset.add_argument("-cf", "--charset-file",
                             dest="charset_file", help=docstrings.HELP_CHARSET_FILE)

    # Mutually exclusive arguments group for input
    arg_input = arg_parser.add_mutually_exclusive_group(required=True)
    arg_input.add_argument("-pa", "--page-address",
                           dest="page_address", help=docstrings.HELP_PAGE_ADDRESS)
    arg_input.add_argument("-af", "--address-file",
                           dest="address_file", help=docstrings.HELP_ADDRESS_FILE)
    arg_input.add_argument("-t", "--text",
                           dest="text_exact", help=docstrings.HELP_TEXT_EXACT)
    arg_input.add_argument("-tr", "--text-random",
                           dest="text_random", help=docstrings.HELP_TEXT_RANDOM)
    arg_input.add_argument("-tf", "--text-file",
                           dest="text_file", help=docstrings.HELP_TEXT_FILE)

    # Now, parse!
    command_line = arg_parser.parse_args()

    charset_modes = {'binary': '01',
                     'morse': ' .-',
                     'borges': 'abcdefghijlmnoprstuvyz, .',
                     'classic': string.ascii_lowercase + ', .',
                     'full': string.digits + string.ascii_letters + ' ' + string.punctuation,
                     'unicode': generate_unicode_string('regular')}

    # Figure out what characters to use according to arg_charset group
    if command_line.charset_mode and command_line.charset_mode in charset_modes:        # -cm
        characters = charset_modes[command_line.charset_mode]

    elif command_line.charset:                                                          # -c
        characters = command_line.charset

    elif command_line.charset_file:                                                     # -cf
        return DataFile(command_line.charset_file).load()

    else:
        raise NotImplementedError(docstrings.ERROR_CHARSET_MODE_NOT_IMPLEMENTED)

    # Figure out what text to use if any specified according to -t, -tr, -tf arguments
    if command_line.text_exact:                                                         # -t
        page_text = command_line.text_exact

    elif command_line.text_random:                                                      # -tr
        page_text = command_line.text_random

    elif command_line.text_file:                                                        # -tf
        text_file = DataFile(command_line.text_file)
        page_text = text_file.load()

    else:
        page_text = None

    # Figure out what address to use if any specified according to -a, -af arguments
    if command_line.page_address:                                                       # -pa
        page_address = command_line.page_address

    elif command_line.address_file:                                                     # -af
        address_file = DataFile(command_line.address_file)
        page_address = address_file.load()

    else:
        page_address = None

    # Validate if page_text exists and consists of characters
    if page_text and is_invalid_input(page_text, characters):
        raise NotImplementedError(docstrings.ERROR_TEXT_NOT_IN_CHARSET)

    # Validate if page_address exists and consists of characters
    if page_address and is_invalid_input(page_address, characters):
        raise NotImplementedError(docstrings.ERROR_ADDRESS_NOT_IN_CHARSET)

    # Instantiate a page, either page_text or page_address should be None
    current_page = Page(characters, page_text, page_address)

    # Getting data out
    data_to_write = 'SOMETHING WENT WRONG'  # Just in case

    if page_address:
        current_page.get_page_text_by_address()
        data_to_write = current_page.page_text

    elif page_text and (command_line.text_exact or command_line.text_file):
        current_page.get_address_by_page_text()
        data_to_write = current_page.address

    elif page_text and command_line.text_random:
        current_page.get_address_by_page_text_random()
        data_to_write = current_page.address

    if command_line.output_file:
        storage = DataFile(command_line.output_file, data_to_write)
        storage.save()

    print(data_to_write)


def text_to_integer(text):
    """
    Converts any text string to an integer,
    for example: 'Hello, world!' to 2645608968347327576478451524936
    """

    # byteorder should be the same as in integer_to_text(), if you want to change it to 'big', change it there too
    return int.from_bytes(bytes(text, 'utf-8'), byteorder='little')


def integer_to_text(number):
    """
    Converts an integer to a text string,
    for example: 2645608968347327576478451524936 to 'Hello, world!'
    Won't convert negative integers
    """

    # byteorder should be the same as in text_to_integer(), if you want to change it to 'big', change it there too
    text = number.to_bytes((number.bit_length() + 7) // 8, byteorder='little')

    return text.decode("utf-8")


def integer_to_base(number, base_string):
    """
    Converts base10 integer to baseX integer (where X is the length of base_string, say X for '0123' is 4),
    for example: 2645608968347327576478451524936 (Which is 'Hello, world!') to 21646C726F77202C6F6C6C6548 (base16),
    does not account for negative numbers
    """

    digits = []
    base_length = len(base_string)

    while number:
        digits.append(base_string[number % base_length])
        number //= base_length

    return ''.join(list(reversed(digits)))


def base_to_integer(base_number, base_string):
    """
    Converts baseX integer to base10 integer (where X is the length of base_string, say X for '0123' is 4),
    for example: 21646C726F77202C6F6C6C6548 (base16) to 2645608968347327576478451524936 (Which is 'Hello, world!'),
    does not account for negative numbers
    """

    number = 0

    for digit in str(base_number):
        number = number * len(base_string) + base_string.index(digit)

    return number


def is_invalid_input(string_one, string_two):
    """
    Checks if the first string does not consist only of characters from the second string
    """

    for character in string_one:

        if character not in string_two and character != '\t':  # Dealing with address formatting

            return True

    return False


def generate_unicode_string(mode=None):
    """
    Generates unicode string that can be used to encode and decode integers
    """

    # Used for page generation
    if mode == 'regular' or not mode:
        # No control characters
        skip_categories = ('Cc', 'Cf', 'Cs', 'Co', 'Cn',
                           'Zl', 'Zp')

    # Used for address generation, not implemented yet
    elif mode == 'address':
        # No control, no marks, no punctuation, no symbols, no separators
        skip_categories = ('Cc', 'Cf', 'Cs', 'Co', 'Cn',
                           'Mn', 'Mc', 'Me',
                           'Pc', 'Pd', 'Ps', 'Pe', 'Pi', 'Pf', 'Po',
                           'Sm', 'Sc', 'Sk', 'So',
                           'Zl', 'Zs', 'Zp',)

    else:
        raise NotImplementedError("""Unknown mode specified for unicode string generator""")

    # Return a string that consists only of characters that has category not listed in skip_categories
    # As of 2017/04/02, maxunicode on most systems is 1114111
    return ''.join(filter(lambda x: category(x) not in skip_categories, map(chr, range(maxunicode))))

if __name__ == '__main__':
    main()
