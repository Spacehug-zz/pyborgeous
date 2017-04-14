PROGRAM_DESCRIPTION = """
pyborgeous is an implementation of Jorge Luis Borges' Library of Babel
"""
PROGRAM_EPILOG = """
         _                               
 ___ _ _| |_ ___ ___ ___ ___ ___ _ _ ___ 
| . | | | . | . |  _| . | -_| . | | |_ -|
|  _|_  |___|___|_| |_  |___|___|___|___|
|_| |___|           |___|              

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
Build the library using pre-defined charset mode.
Usage: -cm borges
Choices: binary, morse, borges, classic, full, unicode, unicode_short
If you want to use custom charset, use -c 'abcde' or -cf 'charset.txt'

"""
HELP_CHARSET = """
Build the library using any custom charset
Usage: -c '0123456789ABCDEF'
Don't use \\t (ASCII TAB) control character in your charset, or there will be trouble with address' formatting

"""
HELP_CHARSET_FILE = """
Build the library using a custom charset from the file
Usage: -cf 'charset.txt'
Don't use \\t (ASCII TAB) control character in your file, or there will be trouble with address' formatting

"""
HELP_PAGE_ADDRESS = """
Find a page by address
Usage: -pa <LONG ADDRESS>

"""
HELP_ADDRESS_FILE = """
Find a page by an address from the file
Format should be: room\\tbookcase[0-3]\\tshelf[0-4]\\tbook[0-31]\\tpage_number[0-409]
\\t is ASCII TAB control character, not literal '\\t'
Usage: -af 'address.txt'

"""
HELP_TEXT_EXACT = """
Find a page that contains only the text and nothing else (the rest of a page is filled with spaces)
Usage: -t 'The first colony on Mars was founded in 2031'
Text longer than 3200 symbols will be truncated

"""
HELP_TEXT_RANDOM = """
Find a page that contains the text plus random words/symbols
Usage: -tr 'The first colony on Mars was founded in 2031.'
Text longer than 3200 symbols will be truncated

"""
HELP_TEXT_FILE = """
Find a page that contains only the text from a file and nothing else
Usage: -tf 'text.txt'
Note: Text longer than 3200 symbols will be truncated

"""
ERROR_PAGE_TO_ADDRESS_UNKNOWN_MODE = """
An unknown page filling mode specified for the page less than 3200 characters
Seeing this error message is not normal

"""
ERROR_CHARSET_MODE_NOT_IMPLEMENTED = """
Either this mode is not implemented, or you have a typo in a case-sensitive mode name

"""
ERROR_TEXT_NOT_IN_CHARSET = """
There is at least one character in the text that is not in the charset

"""
ERROR_ADDRESS_NOT_IN_CHARSET = """
There is at least one character in the address that is not in the charset

"""
