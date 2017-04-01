==========
pyborgeous
==========
pyborgeous is an implementation of https://en.wikipedia.org/wiki/The_Library_of_Babel.

This library can utilize all printable Unicode characters.



**Common usage examples**:


``pyborgeous -m classic -s 'The first colony on mars was founded in 2035.' -d dump.txt``

This will produce an address at which in the library the page with said string (the remaining characters of the page are spaces) is. Also, it will print the address in terminal window and dump it to specified file.


``pyborgeous -c ' -.' -sf 'morsetext.txt'``

This will produce an address at which in the library the page with a string from file is. Beware, if there are other characters than space, dash and dot, the script will fail.


``pyborgeous -cf charset.txt -sr ' Putin is a clone '``

Same as previous, but the charset will be taken from specified file and the string will be surrounded by random characters from that file. Beware that the same rule applies: if the string contains characters that are not in charset provided in the file, the script will fail.

``pybogeous -c unicode -p <**Really long address, don't bother type it in, better use -pf 'file.txt' or copy-paste.**>``
This will generate the exact page on given address. The address should be in the same characters as specified charset,
e.g. unicode in this case.



**Example**:

``pyborgeous -m full -s 'Elon Musk became the president of planet Earth in 2029'``

**Produces address**:


``<Really long string of symbols>       1       4       16      101``


Which means the page with this text:

``Elon Musk became the president of planet Earth in 2029``

is in that room (long address)
2nd bookcase, 5th shelf from the top, 17th book from the left, on the page number 102
The address is stored like 'Room' 1 4 16 101 since computer counts from zero.