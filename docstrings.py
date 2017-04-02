program_description_text = """
pyborgeous is an implementation of Jorge Luis Borges' Library of Babel
"""
program_epilog_text = """
         _                               
 ___ _ _| |_ ___ ___ ___ ___ ___ _ _ ___ 
| . | | | . | . |  _| . | -_| . | | |_ -|
|  _|_  |___|___|_| |_  |___|___|___|___|
|_| |___|           |___|              

Check http://github.com/Spacehug/pyborgeous for updates

"""
help_help = """
Show this help message and exit
Usage: -h

"""
help_version = """
Show program version number and exit
Usage: -v

"""
help_output = """
Output the result to specified file
Usage: -o 'result.txt'

"""
help_charset_mode = """
Build the library in given mode
Usage: -m borges
Choices: binary, morse, borges, classic, full, unicode
If you want to use custom charset, use -c 'abcde' or -cf 'charset.txt'

"""
help_charset = """
Build the library using custom charset
Usage: -c '0123456789ABCDEF'
Warning: don't use \\t (ASCII TAB) control character, or there will be trouble.

"""
help_charset_file = """
Build the library using custom charset from a file
Usage: -cf 'charset.txt'
Warning: don't use \\t (ASCII TAB) control character in your file, or there will be trouble.

"""
help_page_address = """
Find a page by address
Usage: -pa <LONG ADDRESS>

"""
help_address_file = """
Find a page by address from a file
Format should be: room\\tbookcase[1-4]\\tshelf[1-5]\\tbook[1-32]\\tpage_number[1-410]
\\t is ASCII TAB control character, not literal '\\t'
Usage: -af 'address.txt'

"""
help_text_exact = """
Find a page that contains only the text given and nothing else
Usage: -t 'The first colony on Mars was founded in 2031'
Note: Text longer than 3200 symbols will be truncated

"""
help_text_random = """
Find a page that contains the text given, along with random words/symbols
Usage: -tr 'The first colony on Mars was founded in 2031.'
Note: Text longer than 3200 symbols will be truncated

"""
help_text_file = """
Find a page that contains only the text from a file and nothing else
Usage: -tf 'text.txt'
Note: Text longer than 3200 symbols will be truncated

"""
