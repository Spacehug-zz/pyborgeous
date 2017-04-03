PROGRAM_DESCRIPTION = """
pyborgeous is an implementation of Jorge Luis Borges' Library of Babel
"""
PROGRAM_EPILOG = """
         _                               
 ___ _ _| |_ ___ ___ ___ ___ ___ _ _ ___ 
| . | | | . | . |  _| . | -_| . | | |_ -|
|  _|_  |___|___|_| |_  |___|___|___|___|
|_| |___|           |___|              

Check http://github.com/Spacehug/pyborgeous for updates

"""
HELP_HELP = """
Show this help message and exit
Usage: -h

"""
HELP_VERSION = """
Show program version number and exit
Usage: -v

"""
HELP_OUTPUT = """
Output the result to specified file
Usage: -o 'result.txt'

"""
HELP_CHARSET_MODE = """
Build the library in given mode
Usage: -m borges
Choices: binary, morse, borges, classic, full, unicode
If you want to use custom charset, use -c 'abcde' or -cf 'charset.txt'

"""
HELP_CHARSET = """
Build the library using custom charset
Usage: -c '0123456789ABCDEF'
Warning: don't use \\t (ASCII TAB) control character, or there will be trouble.

"""
HELP_CHARSET_FILE = """
Build the library using custom charset from a file
Usage: -cf 'charset.txt'
Warning: don't use \\t (ASCII TAB) control character in your file, or there will be trouble.

"""
HELP_PAGE_ADDRESS = """
Find a page by address
Usage: -pa <LONG ADDRESS>

"""
HELP_ADDRESS_FILE = """
Find a page by address from a file
Format should be: room\\tbookcase[1-4]\\tshelf[1-5]\\tbook[1-32]\\tpage_number[1-410]
\\t is ASCII TAB control character, not literal '\\t'
Usage: -af 'address.txt'

"""
HELP_TEXT_EXACT = """
Find a page that contains only the text given and nothing else
Usage: -t 'The first colony on Mars was founded in 2031'
Note: Text longer than 3200 symbols will be truncated

"""
HELP_TEXT_RANDOM = """
Find a page that contains the text given, along with random words/symbols
Usage: -tr 'The first colony on Mars was founded in 2031.'
Note: Text longer than 3200 symbols will be truncated

"""
HELP_TEXT_FILE = """
Find a page that contains only the text from a file and nothing else
Usage: -tf 'text.txt'
Note: Text longer than 3200 symbols will be truncated

"""
ERROR_CHARSET_MODE_NOT_IMPLEMENTED = """
This mode is not implemented yet

"""
ERROR_TEXT_NOT_IN_CHARSET = """
There is at least one character in text that is not in the charset

"""
ERROR_ADDRESS_NOT_IN_CHARSET = """
There is at least one character in address that is not in the charset

"""