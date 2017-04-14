==========
pyborgeous
==========
pyborgeous is an implementation of https://en.wikipedia.org/wiki/The_Library_of_Babel.

The library contains all the pages of all the books ever written,
the books being written, and the books that will be written in the future.

**Install**:
``pip install pyborgeous``
or
``pip install git+https://github.com/Spacehug/pyborgeous.git``

**Example**:
``pyborgeous -cm unicode -t 'The first colony on Mars was founded in 2027.'``
- Produces address -
``<Really long string of symbols>       2       0       22      152``
Which means the page with the text "The first colony on Mars was founded in 2027." is in the room number (long address),
3rd bookcase, 1st shelf from the top, 23th book from the left, on the page number 153.

**Specials**:
``-cm unicode_short``
The mode is used to generate an address, the page can contain any printable unicode character (same as
-cm unicode) but the address contains only unicode characters that are not symbols, punctuation, marks and so on.
