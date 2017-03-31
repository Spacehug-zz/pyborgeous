# Open-source implementation of Jorge Luis Borges' Library of Babel that can utilize all printable Unicode characters
# Started 2017/03/27

import helpers
import random


class Page:

    # [Pages per book, books per shelf, shelves per bookcase, bookcases per room]
    library_configuration = [410, 32, 5, 4, 0]
    # [Characters per page, characters per title]
    page_configuration = [3200, 25]

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

    def get_page_text_by_address(self):
        room, bookcase, shelf, book, page_number = self.address.split('\t')
        magic_number = helpers.base_to_int(room, self.encode_string)
        magic_number = magic_number * self.library_configuration[3] + int(bookcase)
        magic_number = magic_number * self.library_configuration[2] + int(shelf)
        magic_number = magic_number * self.library_configuration[1] + int(book)
        magic_number = magic_number * self.library_configuration[0] + int(page_number)
        self.text = helpers.int_to_string(magic_number)
        return self.text

    def get_address_by_page_text(self):
        space = ' '
        if len(self.text) < self.page_configuration[0]:
            self.text += space * (self.page_configuration[0] - len(self.text))
        elif len(self.text) > self.page_configuration[0]:
            self.text = self.text[:self.page_configuration[0]]
        magic_number = helpers.string_to_int(self.text)
        self.address = '\t'.join(self.coordinates(magic_number))
        return self.address

    def get_address_by_page_text_random(self):
        if len(self.text) < self.page_configuration[0]:
            postfix_range = random.randrange(self.page_configuration[0] - len(self.text) - 1)
            prefix_range = self.page_configuration[0] - len(self.text) - postfix_range
            prefix = ''.join(random.choice(self.encode_string) for a in range(prefix_range))
            postfix = ''.join(random.choice(self.encode_string) for b in range(postfix_range))
            self.text = prefix + self.text + postfix
        elif len(self.text) > self.page_configuration[0]:
            self.text = self.text[:self.page_configuration[0]]
        magic_number = helpers.string_to_int(self.text)
        self.address = '\t'.join(self.coordinates(magic_number))
        return self.address

    def coordinates(self, magic_number):
        address = []
        for value in self.library_configuration:
            if value == 0:
                address.append(helpers.int_to_base(magic_number, self.encode_string))
            else:
                result_value = magic_number % value
                magic_number = - (magic_number - result_value) // - value
                address.append(str(result_value))
        address.reverse()
        return address


def run_script():
    data_to_write = ''
    current_page = Page(helpers.get_encode_string(),
                        helpers.get_address(),
                        helpers.get_text())

    if helpers.command_line.search_text:
        current_page.get_address_by_page_text()
        data_to_write = current_page.address
        print(current_page.address)
    elif helpers.command_line.text_file:
        current_page.get_address_by_page_text()
        data_to_write = current_page.address
        print(current_page.address)
    elif helpers.command_line.search_text_random:
        current_page.get_address_by_page_text_random()
        data_to_write = current_page.address
        print(current_page.address)
    elif helpers.command_line.address or helpers.command_line.address_file:
        current_page.get_page_text_by_address()
        data_to_write = current_page.text
        print(current_page.text)

    if helpers.command_line.file:
        storage = helpers.DataFile(helpers.command_line.file, data_to_write)
        storage.save()
        print("File " + helpers.command_line.file + " has been written.")


run_script()

if __name__ == '__main__' and helpers.command_line.test:
    pass
