from math import ceil


class Paginator:
    def __init__(self, lst, page=1, per_page=1) -> None:
        self.lst = lst
        self.page = page
        self.per_page = per_page
        self.length = len(lst)
        self.pages = ceil(self.length / self.per_page)

    def get_slice(self):
        start = (self.page - 1) * self.per_page
        stop = start + self.per_page
        return self.lst[start: stop]

    def get_page(self):
        page_items = self.get_slice()
        return page_items

    def has_next(self):
        if self.page < self.length:
            return self.page + 1
        return False
        
    def has_previous(self):
        if self.page > 1:
            return self.page - 1
        return False