# Open-source implementation of Jorge Luis Borges' Library of Babel that can utilize all printable Unicode characters
# Started 2017/03/27

import helpers
# import random


class Page:

    characters_per_title = 25
    characters_per_page = 3200
    pages_per_book = 410
    books_per_shelf = 32
    shelves_per_bookcase = 5
    bookcases_per_room = 4

    def __init__(self, encode_string, address, text):
        self.encode_string = encode_string
        if address:
            self.address = address
            self.text = None
        elif text:
            for character in text:
                if character not in encode_string:
                    raise NotImplementedError("""Some letters of the text does not present in encoding string.
                    I can't map them for you at the moment.
                    Pick another mode or modify your search string.""")
                else:
                    self.text = text
                    self.address = None

    def get_page_text_by_address(self, address):
        pass

    def get_address_by_page_text(self, text):
        pass

    def get_address_by_page_text_random(self, text):
        pass

    def get_page_title_by_address(self, address):
        pass

current_page = Page(helpers.get_encode_string(),
                    helpers.get_address(),
                    helpers.get_text())

if __name__ == '__main__' and helpers.command_line.test:
    print(current_page.__dict__)
